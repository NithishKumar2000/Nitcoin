// Nitcoin ICO

//Version of the Compiler
pragma solidity ^0.4.11;

//contract
contract Nitcoin_ico
{
    Total number of Nitcoins
    uint public total_coins=1000000;
    
    // 1 USD = 1000 Nitcoins
    uint public usd_to_nitcoin=1000;
    
    // Total coins sold til now 
    uint public total_coins_bought=0;
    
    // Mapping the investor address to usd and Nitcoins
    mapping(address=>uint)equity_nitcoins;
    mapping(address=>uint)equity_usd;
    
    // Using a modifier function to check if there is enough number of nitcoins left when a investor wants to purchase the coin
    modifier can_buy_nitcoins(uint usd_invested){
        require(usd_invested*usd_to_nitcoin+total_coins_bought<=total_coins);  //Require is used to check if there is enough nitcoins left is the system, 
        _;}                                                                     //the modifier function is only executed if the require function fails
    
    // Functioj to get the amount the inverstor has in nitcoins
    function equity_in_nitcoins(address inverstor)external constant returns(uint){
        return equity_nitcoins[inverstor];
    }
        
    //Function to get the equity of the ivestor in usd_to_nitcoin
    function equity_in_usd(address inverstor)external constant returns(uint){
        return equity_usd[inverstor];
    }
    
    // Buyuing nitcoins
    function buy_nitcoins(address investor, uint usd_invested) external 
    can_buy_nitcoins(usd_invested){
        uint nitcoins_bought=usd_invested*usd_to_nitcoin;
        equity_nitcoins[investor]+=nitcoins_bought;
        equity_usd[investor]=equity_nitcoins[investor]/1000;
        total_coins_bought+=equity_nitcoins;
    }
    
    // Selling nitcoins
    function sell_nitcoins(address investor,uint nitcoins_sold) external{
        uint nitcoins_bought=usd_invested*usd_to_nitcoin;
        equity_nitcoins[investor]-=nitcoins_sold;
        equity_usd[investor]=equity_nitcoins[investor]/1000;
        total_coins_bought-=nitcoins_sold;
    }
}