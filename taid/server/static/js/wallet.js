var app = new Vue({
    el: '#app',
    data: {
        walletAddress: '',
        transactions: [],
    },
    mounted() {
        let wallet = getParameterByName('wallet');
        this.walletAddress = wallet;
        this.fetchRecipient(wallet);
    },
    methods: {
        async fetchRecipient(wallet) {
            try {
                if (!wallet) {
                    return false;
                }
                const response = await axios.get(`http://taid.kr/view/chain/${wallet}`);
                this.getTransactions(response.data);
            } catch (error) {
                console.error(error);
            }
        },
        getTransactions(data) {
            this.transactions = [];
            for (let i = 0; i < data.length; i++) {
                let transaction = data[i].transaction;
                this.transactions.push({
                    index: data[i].block_index,
                    type: (transaction.sender === this.walletAddress) ? 'Sent' : 'Received',
                    amount: transaction.amount,
                    message: transaction.message,
                    purpose: transaction.purpose,
                    recipient: transaction.recipient,
                    sender: transaction.sender
                });
            }
        }
    }
});
