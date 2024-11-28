// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

// Import OpenZeppelin Libraries
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title NFT Marketplace
/// @notice Enables minting, listing, and trading of NFTs
contract NFTMarketplace is ERC721, Ownable {
    uint256 public tokenIdCounter;
    uint256 public listingFee = 0.01 ether;

    struct NFT {
        uint256 id;
        address owner;
        uint256 price;
        bool isListed;
    }

    mapping(uint256 => NFT) public nfts;

    // Events
    event NFTMinted(address indexed owner, uint256 indexed tokenId);
    event NFTListed(uint256 indexed tokenId, uint256 price);
    event NFTPurchased(address indexed buyer, uint256 indexed tokenId, uint256 price);

    constructor() ERC721("QuantumNFT", "QNFT") {}

    /// @notice Mint a new NFT
    /// @param to Address of the NFT recipient
    function mintNFT(address to) external onlyOwner {
        uint256 newTokenId = tokenIdCounter++;
        _mint(to, newTokenId);
        nfts[newTokenId] = NFT(newTokenId, to, 0, false);
        emit NFTMinted(to, newTokenId);
    }

    /// @notice List an NFT for sale
    /// @param tokenId ID of the NFT to list
    /// @param price Sale price of the NFT
    function listNFT(uint256 tokenId, uint256 price) external payable {
        require(msg.sender == ownerOf(tokenId), "Only the owner can list the NFT");
        require(msg.value >= listingFee, "Listing fee required");
        nfts[tokenId].price = price;
        nfts[tokenId].isListed = true;
        emit NFTListed(tokenId, price);
    }

    /// @notice Purchase an NFT
    /// @param tokenId ID of the NFT to purchase
    function purchaseNFT(uint256 tokenId) external payable {
        NFT memory nft = nfts[tokenId];
        require(nft.isListed, "NFT is not listed");
        require(msg.value >= nft.price, "Insufficient payment");

        address seller = nft.owner;
        payable(seller).transfer(msg.value);
        _transfer(seller, msg.sender, tokenId);

        nfts[tokenId].owner = msg.sender;
        nfts[tokenId].isListed = false;

        emit NFTPurchased(msg.sender, tokenId, msg.value);
    }
}
