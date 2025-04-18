from pathlib import Path
from dataclasses import dataclass
import subprocess
import sys
from time import sleep, time
from typing import Optional
from psutil import NoSuchProcess, Process
import os


@dataclass
class UtilisationStat:
    run_no: int
    time_s: float
    rss: int
    vms: int
    # Whether or not this information exists depends on platform - not on Linux it seems
    pfaults: Optional[int]
    pageins: Optional[int]
    cpu_pct: float
    # Whether or not this information is available depends on user privileges
    uss: Optional[int]
    swap: Optional[int]

    @staticmethod
    def csv_header() -> str:
        return "run_no,time_s,rss,vms_kb,pfaults,pageins,cpu_pct,uss,swap"

    def csv_row(self) -> str:
        return f"{self.run_no},{self.time_s},{self.rss},{self.vms},{self.pfaults},{self.pageins},{self.cpu_pct},{self.uss},{self.swap}"


class Benchmark:
    n_warmup: int
    n_iter: int
    # Best effort attempt to watch the process with this frequency. This will not be terribly accurate but will work *well enough*
    peek_ms: float
    script_path: Path
    output_file_path: Path
    is_root: bool
    args: list[str]

    def __init__(
        self,
        script_path: Path,
        output_file_path: Path,
        peek_ms=100,
        n_warmup=2,
        n_iter=30,
        args: list[str] = [],
    ):
        self.n_warmup = n_warmup
        self.n_iter = n_iter
        self.peek_ms = peek_ms
        self.script_path = script_path
        self.output_file_path = output_file_path
        self.is_root = os.getuid() == 0
        self.args = args

        if not self.is_root:
            print(
                "Warning: running in non-super user mode, cannot gather USS and swap statistics"
            )

    def _do_run(self, run_no: int):
        data_readings: list[UtilisationStat] = []
        spawned_process = subprocess.Popen(
            [sys.executable, self.script_path.absolute().resolve(), *self.args],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        monitored_process = Process(spawned_process.pid)
        start_time = monitored_process.create_time()

        while spawned_process.poll() is None:
            try:
                memory_utilisation = (
                    monitored_process.memory_full_info()
                    if self.is_root
                    else monitored_process.memory_info()
                )
                cpu_utilisation = monitored_process.cpu_percent()
                swap = getattr(memory_utilisation, "swap", None)
                uss = getattr(memory_utilisation, "uss", None)
                pageins = getattr(memory_utilisation, "pageins", None)
                pfaults = getattr(memory_utilisation, "pfaults", None)

                data_readings.append(
                    UtilisationStat(
                        run_no=run_no,
                        time_s=time() - start_time,
                        cpu_pct=cpu_utilisation,
                        pageins=pageins,
                        pfaults=pfaults,
                        rss=memory_utilisation.rss,
                        vms=memory_utilisation.vms,
                        uss=uss,
                        swap=swap,
                    )
                )
                sleep(self.peek_ms / 1000)
            except NoSuchProcess:
                break

        if spawned_process.returncode != 0:
            raise RuntimeError(
                f"Exit code: {spawned_process.returncode} for child process"
            )

        return data_readings

    def run(self):
        for i in range(self.n_warmup):
            print(f"Running warmup run {i + 1}/{self.n_warmup}")
            self._do_run(i)

        with open(self.output_file_path, "w") as outfile:
            print(UtilisationStat.csv_header(), file=outfile)
            for i in range(self.n_iter):
                print(f"Running iteration {i + 1}/{self.n_iter}")
                result = self._do_run(i)
                for row in result:
                    print(row.csv_row(), file=outfile)
