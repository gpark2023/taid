var app = new Vue({
    el: '#app',
    data: {
        recipient: null,
        donorName: '',
        amount: '',
    },
    mounted() {
        let wallet = getParameterByName('wallet');
        this.fetchRecipient(wallet);
    },
    methods: {
        async fetchRecipient(wallet) {
            try {
                if (!wallet) {
                    return false;
                }
                const response = await axios.get(`http://taid.kr/view/recipient/${wallet}`);
                this.recipient = response.data[0];
            } catch (error) {
                console.error(error);
            }
        },
        async donate() {
            try {
                if (!this.donorName) {
                    alert('Input Wallet Address');
                    return false;
                } else if (!this.amount) {
                    alert('Input Amount');
                    return false;
                }
                const url = new URL(window.location.href);
                const url_param = url.searchParams;
                reci_wallet = url_param.get('wallet');
                let donate_req = {
                    purpose : "Donation Response",
                    message : "Donation",
                    recipient : reci_wallet,
                    sender : this.donorName,
                    amount : this.amount
                };
                axios.post('http://3.101.138.234:1000/transactions/new', donate_req);
                alert("Donate Complete!");
                movePage(`recipient.html`);
            } catch(error) {
                console.error(error);
            }
        },
    }
});
