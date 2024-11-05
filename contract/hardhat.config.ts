import * as dotenv from "dotenv";

import {HardhatUserConfig, task} from "hardhat/config";
import "@nomicfoundation/hardhat-chai-matchers";
import "@nomicfoundation/hardhat-verify";
import "@openzeppelin/hardhat-upgrades";
import "@typechain/hardhat";
import "hardhat-gas-reporter";
import "solidity-coverage";

dotenv.config();

task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
    const accounts = await hre.ethers.getSigners();
    for (const account of accounts) {
        console.log(account.address);
    }
});

const config: HardhatUserConfig = {
    solidity: {
        compilers: [
            {
                version: "0.8.26",
                settings: {
                    optimizer: {
                        enabled: true,
                        runs: 100000,
                    },
                    viaIR: true
                },
            },
        ],
    },
    networks: {
        localhost: {
            accounts: [process.env.DEPLOYER_KEY!],
        },
        forking: {
            url: "http://127.0.0.1:8545",
            accounts: [process.env.DEPLOYER_KEY!],
        },
        blast: {
            url: "https://rpc.blast.io",
            accounts: [process.env.DEPLOYER_KEY!],
        },
        fantom: {
            url: "https://rpc.ftm.tools",
            accounts: [process.env.DEPLOYER_KEY!],
        },
        fantom_test: {
            url: "https://rpc.testnet.fantom.network/",
            accounts: [process.env.DEPLOYER_KEY!],
        },
        sepolia: {
            url: `https://sepolia.infura.io/v3/${process.env.INFURA_API_KEY}`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        mainnet: {
            url: `https://ethereum.publicnode.com`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        bsc: {
            url: `https://bsc.rpc.blxrbdn.com`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        polygon: {
            url: `https://polygon-rpc.com/`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        arbitrum: {
            url: `https://arb1.arbitrum.io/rpc`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        avax: {
            url: `https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        kava: {
            url: `https://evm.kava.io`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        zkevm: {
            url: `https://zkevm-rpc.com`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        op: {
            url: `https://optimism.llamarpc.com	`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        base: {
            url: `https://base.llamarpc.com`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
        holesky: {
            url: `https://holesky.gateway.tenderly.co`,
            accounts: [process.env.DEPLOYER_KEY!],
        },
    },
    sourcify: {
        enabled: false,
    },
    gasReporter: {
        enabled: process.env.REPORT_GAS !== undefined,
        currency: "USD",
    },
    etherscan: {
        apiKey: {
            // polygon: process.env.POLYGON_API_KEY!,
            // blast: process.env.BLAST_API_KEY!,
            sepolia: process.env.ETHERSCAN_API_KEY!,
            holesky: process.env.ETHERSCAN_API_KEY!,
        },
        customChains: [
            {
                network: "blast",
                chainId: 81457,
                urls: {
                    apiURL: "https://api.blastscan.io/api",
                    browserURL: "https://blastscan.io",
                },
            },
            {
                network: "sepolia",
                chainId: 11155111,
                urls: {
                    apiURL: "https://api-sepolia.etherscan.io/api",
                    browserURL: "https://sepolia.etherscan.io",
                },
            },
            {
                network: "holesky",
                chainId: 17000,
                urls: {
                    apiURL: "https://api-holesky.etherscan.io/api",
                    browserURL: "https://holesky.etherscan.io",
                },
            },
        ],
    },
};

export default config;
