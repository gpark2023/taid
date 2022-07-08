var app = new Vue({
    el: '#app',
    data: {
        recipient: null,
        donorName: '',
        amount: '',
        good: '',
        shopname: '',
        wallet: ''
    },
    mounted() {
        this.wallet = getParameterByName('wallet');
        this.good = getParameterByName('good');
        this.shopname = getParameterByName('shopName');

    },
    methods: {
        async buy() {
            try {
                if (!this.donorName) {
                    alert('Input Wallet Address');
                    return false;
                } else if (!this.amount) {
                    alert('Input Amount');
                    return false;
                }
                let donate_req = {
                    purpose : "Buy",
                    message : this.good,
                    recipient : this.wallet,
                    sender : this.donorName,
                    amount : this.amount
                };
                axios.post('http://3.101.138.234:1000/transactions/new', donate_req);
                alert("Buy Complete!");
                movePage(`shop.html`);
            } catch(error) {
                console.error(error);
            }
        },
    }
});
