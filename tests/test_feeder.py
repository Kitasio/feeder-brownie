from brownie import Feeder, accounts, exceptions, FeederFactory
from web3 import Web3
import pytest

name = "test"


def test_deploy_factory():
    account = accounts[0]
    factory = FeederFactory.deploy({"from": account})
    tx = factory.createFeeder(
        [accounts[0], accounts[1], accounts[3], accounts[4]],
        [20, 70, 5, 5],
        name,
        {"from": account},
    )
    tx.wait(1)
    print(f"the birds addresses: {factory.getFeeders(account)}")

    tx = factory.createFeeder(
        [accounts[0], accounts[1]],
        [
            20,
            80,
        ],
        name,
        {"from": account},
    )
    tx.wait(1)
    print(f"the birds addresses: {factory.getFeeders(account)[0]}")
    assert factory.getFeeders(account)[1] == 2


def test_alloc_to_wallet_different_length():
    account = accounts[0]
    with pytest.raises(exceptions.VirtualMachineError):
        feeder = Feeder.deploy(
            [accounts[0], accounts[1]], [20, 70, 10], name, {"from": account}
        )


def test_alloc_overflow():
    account = accounts[0]
    feeder = Feeder.deploy(
        [accounts[0], accounts[1]], [20, 80], name, {"from": account}
    )

    funder = accounts[4]
    print("funding account with 10 ether")
    funder.transfer(feeder.address, "10 ether")
    print("user has 20 percent alloc, trying to withdraw 30...")
    with pytest.raises(exceptions.VirtualMachineError):
        feeder.withdraw(Web3.toWei(3, "ether"), {"from": account})
    print("He failed")
    print("trying to get 10 percent")
    feeder.withdraw(Web3.toWei(1, "ether"), {"from": account})
    assert feeder.balance() == 9 * 10 ** 18
    print("success")
    print("funding with another 10 ether")
    funder.transfer(feeder.address, "10 ether")
    assert feeder.balance() == 19 * 10 ** 18
    print("s 19 ether, user should be able to get 3")
    print("trying to get 4")
    with pytest.raises(exceptions.VirtualMachineError):
        feeder.withdraw(Web3.toWei(4, "ether"), {"from": account})
    print("He failed")
    print("trying to get 3")
    feeder.withdraw(Web3.toWei(3, "ether"), {"from": account})
    assert feeder.balance() == 16 * 10 ** 18
    print("nice")


def test_fund_and_withdraw():
    account = accounts[0]
    feeder = Feeder.deploy(
        [accounts[0], accounts[1]], [20, 80], name, {"from": account}
    )

    funder = accounts[4]
    funder.transfer(feeder.address, "10 ether")

    initial_balance = account.balance()
    feeder.withdraw(Web3.toWei(2, "ether"), {"from": account})

    assert account.balance() == initial_balance + Web3.toWei(2, "ether")

    # assert feeder.balance() == 8 * 10 ** 18
    # assert feeder.user(account)[1] == Web3.toWei(2, "ether")


def test_bad_actor_withdraw():
    account = accounts[0]
    feeder = Feeder.deploy(
        [accounts[0], accounts[1]], [20, 80], name, {"from": account}
    )

    funder = accounts[4]
    funder.transfer(feeder.address, "3 ether")

    bad_actor = accounts[5]
    with pytest.raises(exceptions.VirtualMachineError):
        feeder.withdraw(1 * 10 ** 18, {"from": bad_actor})
