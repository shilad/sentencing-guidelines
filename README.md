# Sentencing-guidelines
Retrieves data about sentencing guidelines from the pacer repo.

# Instructions

1. Clone this repo:

    ```
    git clone https://github.com/shilad/sentencing-guidelines.git
    ```
 
2. Install necessary dependencies (from juriscraper docs)

    ```
    # On Ubuntu/Debian Linux:
        sudo apt-get install libxml2-dev libxslt-dev libyaml-dev
    # On macOS with Homebrew <https://brew.sh>:
        brew install libyaml
    
    # -- Install PhantomJS
    # On Ubuntu/Debian Linux
        wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2
        tar -x -f phantomjs-1.9.7-linux-x86_64.tar.bz2
        sudo mv phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/local/bin
        rm -r phantomjs-1.9.7*  # Cleanup
    # On macOS with Homebrew:
        brew install phantomjs
    
    # create a directory for logs (this can be skipped, and no logs will be created)
    sudo mkdir -p /var/log/juriscraper

    pip install -f requirements.txt
    ```

3. IF YOU WANT TO RECREATE `case_queries.csv`: Create the queries (expects `mergedData.csv`) in main directory.

    ```
   python ./construct_pacer_queries.py
    ```

4. Run the scraper. It is safe to stop and restart it as long as you preserve the pacer_results.json file.

    ```
   python ./process_queries.py
    ```
