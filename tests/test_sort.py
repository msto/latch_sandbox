from pathlib import Path

from fgpyo.sam.builder import SamBuilder
from fgpyo.sam import reader
from fgpyo.sam import writer
from latch.types.file import LatchFile
from latch.types.directory import LatchOutputDir

from wf.sort import sort_bam_task


def test_sort_bam_task(tmp_path: Path):
    """
    `sort_bam_task` should produce a coordinate-sorted BAM file.
    """
    unsorted_bam_path = tmp_path / "unsorted.bam"

    builder = SamBuilder()
    with writer(path=unsorted_bam_path, header=builder.header) as bam_writer:
        for start in [100, 300, 200]:
            read = builder.add_single(chrom="chr1", start=start)
            bam_writer.write(read)

    sorted_bam_latchfile = sort_bam_task(
        sam=LatchFile(path=unsorted_bam_path),
        output_directory=LatchOutputDir("latch:///fake_output_directory/"),
    )

    with reader(path=sorted_bam_latchfile.path) as bam_reader:
        reads = [r for r in bam_reader]

    assert len(reads) == 3
    assert [read.reference_start for read in reads] == [100, 200, 300]
