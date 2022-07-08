var app = new Vue({
    el: '#app',
    data: {
        transactions: []
    },
    mounted() {
        this.fetchChains();
    },
    methods: {
        async fetchChains() {
            try {
                const response = await axios.get('http://taid.kr/view/all_chain');
                this.getTransactions(response.data.chain);
            } catch (error) {
                console.error(error);
            }
        },
        viewWalletDetail(wallet) {
            movePage(`wallet_transaction.html?wallet=${wallet}`);
        },
        getTransactions(chains) {
            this.transactions = [];
            for (let i = 0; i < chains.length; i++) {
                for (let j = 0; j < chains[i].transactions.length; j++) {
                    this.transactions.push({
                        index: chains[i].index,
                        previousHash: chains[i].previous_hash,
                        proof: chains[i].proof,
                        timestamp: chains[i].timestamp,
                        amount: chains[i].transactions[j].amount,
                        sender: chains[i].transactions[j].sender,
                        recipient: chains[i].transactions[j].recipient,
                    });
                }
            }
        }
    }
});
