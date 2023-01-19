#!/bin/bash
set -e

FIFT_PATH="/opt/ton/ton/crypto/fift"
FUNC_PATH="/opt/ton/build/crypto/func"
FIFT_EXE_PATH="/opt/ton/build/crypto/fift"
TESTS_PATH="tests"
OUT_PATH="../out"

export FIFTPATH=$FIFT_PATH/lib

# build smart contracts

$FUNC_PATH \
   -SPA func/stdlib.fc \
        func/op-codes.fc \
        func/utils.fc \
        func/nft-collection.fc \
   -o $OUT_PATH/nft-collection-code.fif

$FUNC_PATH \
   -SPA func/stdlib.fc \
        func/op-codes.fc \
        func/utils.fc \
        func/nft-item.fc \
   -o $OUT_PATH/nft-item-code.fif


# execute fift

$FIFT_EXE_PATH -s $TESTS_PATH/test.fif
