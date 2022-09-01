from dataclasses import dataclass
from typing import Callable


@dataclass
class Program:
    exec: str
    args: Callable[[str, str], list[str]]

    def cmd(self, i: str, o: str) -> list[str]:
        return [self.exec, *self.args(i, o)]


@dataclass
class EncoderAndDecoder:
    name: str
    encoder: Program
    decoder: Program


@dataclass
class CodersSet:
    libjxl: EncoderAndDecoder = EncoderAndDecoder(
        name='libjxl',
        encoder=Program(
            exec='executables/libjxl/cjxl',
            args=lambda i, o: ['--quiet', '--lossless_jpeg=1', i, o]
        ),
        decoder=Program(
            exec='executables/libjxl/djxl',
            args=lambda i, o: ['--quiet', i, o]
        )
    )

    acp: EncoderAndDecoder = EncoderAndDecoder(
        name='acp',
        encoder=Program(
            exec='executables/acp/cjxl',
            args=lambda i, o: ['--quiet', '--lossless_jpeg=1', i, o]
        ),
        decoder=Program(
            exec='executables/acp/djxl',
            args=lambda i, o: ['--quiet', i, o]
        )
    )

    brotli: EncoderAndDecoder = EncoderAndDecoder(
        name='brotli',
        encoder=Program(
            exec='executables/brotli/brotli',
            args=lambda i, o: [i, '-o', o]
        ),
        decoder=Program(
            exec='executables/brotli/brotli',
            args=lambda i, o: ['--decompress', i, '-o', o]
        )
    )

    brunsli: EncoderAndDecoder = EncoderAndDecoder(
        name='brunsli',
        encoder=Program(
            exec='executables/brunsli/cbrunsli',
            args=lambda i, o: [i, o]
        ),
        decoder=Program(
            exec='executables/brunsli/dbrunsli',
            args=lambda i, o: [i, o]
        )
    )

    lepton: EncoderAndDecoder = EncoderAndDecoder(
        name='lepton',
        encoder=Program(
            exec='executables/lepton/lepton',
            args=lambda i, o: [i, o]
        ),
        decoder=Program(
            exec='executables/lepton/lepton',
            args=lambda i, o: [i, o]
        )
    )

    @staticmethod
    def all():
        return [CodersSet.acp, CodersSet.libjxl, CodersSet.brotli, CodersSet.brunsli, CodersSet.lepton]


@dataclass
class ImageInfo:
    path: str
    width: int
    height: int
    bytes: int

    def bpp(self):
        return self.bytes / (self.width * self.height)
