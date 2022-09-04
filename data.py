from dataclasses import dataclass
from typing import Callable


@dataclass
class Program:
    exec: str
    args: Callable[[list[str]], list[str]]

    def cmd(self, params: list[str]) -> list[str]:
        return [self.exec, *self.args(params)]


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
            exec='executables/libjxl/libjxl/tools/cjxl',
            args=lambda params: ['--quiet', '--lossless_jpeg=1', params[0], params[1]]
        ),
        decoder=Program(
            exec='executables/libjxl/libjxl/tools/djxl',
            args=lambda params: ['--quiet', params[0], params[1]]
        )
    )

    acp: EncoderAndDecoder = EncoderAndDecoder(
        name='acp',
        encoder=Program(
            exec='executables/acp/acp/tools/cjxl',
            args=lambda params: ['--quiet', '--lossless_jpeg=1', params[0], params[1]]
        ),
        decoder=Program(
            exec='executables/acp/acp/tools/djxl',
            args=lambda params: ['--quiet', params[0], params[1]]
        )
    )

    acp_coeffs: EncoderAndDecoder = EncoderAndDecoder(
        name='acp-coeffs',
        encoder=Program(
            exec='executables/acp-coeffs/acp-coeffs/tools/cjxl',
            args=lambda params: ['--lossless_jpeg=1', params[0], params[1], params[2]]
        ),
        decoder=Program(
            exec='executables/acp-coeffs/acp-coeffs/tools/djxl',
            args=lambda params: [params[0], params[1], params[2]]
        )
    )

    brotli: EncoderAndDecoder = EncoderAndDecoder(
        name='brotli',
        encoder=Program(
            exec='executables/brotli/brotli',
            args=lambda params: [params[0], '-o', params[1]]
        ),
        decoder=Program(
            exec='executables/brotli/brotli',
            args=lambda params: ['--decompress', params[0], '-o', params[1]]
        )
    )

    brunsli: EncoderAndDecoder = EncoderAndDecoder(
        name='brunsli',
        encoder=Program(
            exec='executables/brunsli/cbrunsli',
            args=lambda params: [params[0], params[1]]
        ),
        decoder=Program(
            exec='executables/brunsli/dbrunsli',
            args=lambda params: [params[0], params[1]]
        )
    )

    lepton: EncoderAndDecoder = EncoderAndDecoder(
        name='lepton',
        encoder=Program(
            exec='executables/lepton/lepton',
            args=lambda params: [params[0], params[1]]
        ),
        decoder=Program(
            exec='executables/lepton/lepton',
            args=lambda params: [params[0], params[1]]
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
