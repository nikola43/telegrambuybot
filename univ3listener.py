if __name__ == "__main__":
    print("Starting bot...")

    # create script for listen uniswap v3 swap events
    univ3listener = UniV3Listener()
    univ3listener.start()
    
    
