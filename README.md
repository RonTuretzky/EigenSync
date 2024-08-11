# EigenSync

EigenSync enables the verification of aggregated BLS signatures by EigenLayer operators on any EVM-compatible chain by mirroring their keys and stakes. This allows developers to grant contract ownership on these chains to EigenLayer operators, a feature previously restricted to the mainnet.

For an in-depth understanding of EigenSync's architecture, visit our [Wiki](https://github.com/Inspector-Butters/EigenSync/wiki).

## Main Components

The EigenSync comprises two main components:

1. Operator Registry Contract
2. Synchronizer Service

### Operator Registry Contract

The Operator Registry is a middleware contract deployed on EVM-compatible chains, designed to host AVS operators' stakes and keys. It allows dApps on these chains to verify aggregated BLS signatures from AVS operators.

The following section outlines how to run tests and deploy the contract.

#### Testing

To test the contract, run the following commands:

```bash
$ git clone https://github.com/Inspector-Butters/EigenSync.git
$ cd contract
$ npm install
$ npx hardhat test
```

#### Deploying the Contract

Add the configuration for the chain you want to deploy on, and add your private key and scanner API key (for verification) in the `.env` file. Then, deploy the contract with the following command:

```bash
$ npx hardhat run ./scripts/deploy.ts --network <NETWORK_NAME>
```

If the verification fails, you can try the following command:

```bash
$ npx hardhat verify <CONTRACT_ADDRESS> --network <NETWORK_NAME> --force
```

###### Deployment operator registry contract on different chains:

| Network  | Deployment Address                              |
|----------|-------------------------------------------------|
| Sepolia  | `0xB3efEc7Fe6b7ae0CDe3abFC46AaBD527F95D390C`    |
| Base     | `0xC62aB311db6B819d05dE464eB338836595f99C8d`    |
| Optimism | `0x01b028f1BF8FC6915D53F762C6Ff905e4AAE6877`    |
| Celo     | `0xf9937cf6EeDA0628b04B9782693D942D58fac165`    |
| Frax     | `0x01b028f1BF8FC6915D53F762C6Ff905e4AAE6877`    |


---

### Synchronizer Service

The Synchronizer is an oracle service that retrieves the AVS operators' keys and stake information from the AVS middleware contracts on the mainnet and records it in the operator registry contract on the destination chain. This service includes one script for operators and two scripts for the aggregator. To install the necessary dependencies, run the following command:

```bash
$ pip install -r requirements.txt
```

#### On Operators

Navigate to the operator directory:

```bash
$ cd operator
```

Create a `KEY_PAIR` and obtain an [Infura key](https://www.infura.io/). Complete the `local_setting.py` file based on the sample provided.

Run the node script:

```bash
$ python node.py
```

#### On Aggregator

Navigate to the aggregator directory:

```bash
$ cd aggregator
```

Create an [Infura key](https://www.infura.io/) and add the address and private key of the account used to deploy the **Operator Registry Contract** (or any account with the `DAO_ROLE` on the contract). Complete the `local_setting.py` file based on the sample provided.

To initiate the process and register the first operator on the **Operator Registry Contract**, run:

```bash
$ python initialization.py
```

To run the aggregator service:

```bash
$ python aggregator.py
```

For more information on the [EigenSDK](https://eigensdk-python.readthedocs.io/en/latest/) used for cryptographic operations, please visit the [Zellular Project](https://www.zellular.xyz/).

---
