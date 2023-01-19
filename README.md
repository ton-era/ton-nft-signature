# TON NFT Signature Contract

TON Token signature contract implementation from [TEP](https://github.com/ton-era/TEPs/blob/master/text/0090-tsc-standard.md).

## Summary

Token Signature Contract (TSC) - is a special type of contract which acts as an agreement between the NFT owner and the  signatory. Leaving a signature on an NFT object serves as a validation by the third party. The signature belongs to its specific NFT and cannot be forwarded to anyone, as it is being a special type of SBT ([TEP 89](https://github.com/ton-blockchain/TEPs/blob/master/text/0085-sbt-standard.md)).

## Motivation

The concept of signing NFT objects is a demanded and natural tool, which has lots of potential applications. For example, an electronic document in the blockchain, that must be signed by interested parties, can be implemented as an NFT object. In this case, the NFT signing concept presented here is a fundamental base of electronic document management on TON blockchain. Another entertaining application has to do with looking at a signature as an autograph. In case a celebrity signs an NFT object, its collectible value will instantly increase, and will also serve as an additional anti-scam verification of the object.

Here one can find one of possible implementations of such an idea. For more information see ([TEP 89](https://github.com/ton-blockchain/TEPs/blob/master/text/0085-sbt-standard.md)).
