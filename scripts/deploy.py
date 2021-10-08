from scripts.helpful_scripts import get_account
from brownie import Feeder, FeederFactory, accounts, config, network

allocations = [50, 50]
# accounts_list = [accounts[0], accounts[1]]
name = "Hello contract"

accounts_list = [
    "0xf839B1cb80F509d98FFd7600a3aDB8e87083B41d",
    "0xAfFA080613F8955612573135e7A4c3A0257c6B58",
]

def deploy():
    account = get_account()
    feeder_factory = FeederFactory.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def createFeeder():
    account = get_account()
    feeder_factory = FeederFactory[-1]
    feeder = feeder_factory.createFeeder(accounts_list, allocations, {"from": account})
    return feeder


def deploy_feeder():
    account = get_account()
    feeder = Feeder.deploy(
        accounts_list,
        allocations,
        name,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    # funder = accounts[4]
    # funder.transfer(feeder.address, "10 ether")
    # print(f"The balance is {feeder.getBalance()/10**18}")
    # print(f"state is: {feeder.user(account)}")
    # tx = feeder.withdraw(0.5 * 10 ** 18, {"from": account})
    # print("withdrawing 1 ether...")
    # tx.wait(1)
    # print(f"state is: {feeder.user(account)}")

    # print(f"The feeder balance is {feeder.getBalance()/10**18}")
    # print(f"The account balance is {account.balance()/10**18}")

    # tx = feeder.withdraw(1.5 * 10 ** 18, {"from": account})
    # print("withdrawing 1 ether...")
    # tx.wait(1)
    # print(f"The feeder balance is {feeder.getBalance()/10**18}")
    # print(f"The account balance is {account.balance()/10**18}")


def main():
    deploy()
    # deploy_feeder()
    # createFeeder()
