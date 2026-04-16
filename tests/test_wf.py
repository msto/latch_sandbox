import shutil
from pathlib import Path

import pytest
from latch.types.file import LatchFile
from latch.types.directory import LatchOutputDir
from pytest_mock import MockerFixture

from wf import assemble_and_sort


@pytest.fixture
def datadir() -> Path:
    """Path to the test data directory."""

    return Path(__file__).parent / "data"


def test_assemble_and_sort(datadir: Path, mocker: MockerFixture) -> None:
    """
    The workflow should complete without error and produce a sorted BAM file.
    """
    r1_fastq_path = datadir / "r1.fastq"
    r2_fastq_path = datadir / "r2.fastq"

    bowtie_path = shutil.which("bowtie2")
    assert bowtie_path is not None, "bowtie2 must be installed locally to test"
    mocker.patch("wf.assemble.BOWTIE_PATH_PREFIX", Path(bowtie_path).parent)

    sorted_bam_latchfile = assemble_and_sort.function(
        read1=LatchFile(path=r1_fastq_path),
        read2=LatchFile(path=r2_fastq_path),
        output_directory="latch://1.account/fake_output_directory/",
    )

    assert Path(sorted_bam_latchfile.path).name == "covid_sorted.bam"
    assert sorted_bam_latchfile.remote_path == "latch://1.account/fake_output_directory/covid_sorted.bam"

