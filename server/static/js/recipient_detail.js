var app = new Vue({
    el: '#app',
    data: {
        wallet: '',
        recipient: null,
    },
    mounted() {
        this.wallet = getParameterByName('wallet');
        this.fetchRecipient(this.wallet);
    },
    methods: {
        async fetchRecipient(wallet) {

            try {
                if (!wallet) {
                    return false;
                }
                const response = await axios.get(`http://taid.kr/view/recipient/${wallet}`);
                this.recipient = response.data[0];
                this.recipient.donation_progress = Math.round(this.recipient.current / this.recipient.required * 100);

                document.documentElement.style.setProperty('--test', String(this.recipient.donation_progress)+"%");
            } catch (error) {
                console.error(error);
            }
        },
        convertTrailMessage(trail) {
            if (trail.type == 'Donation') {
                return `${trail.info.name}이 $${trail.info.amount}를 Donate`;
            } else if (trail.type == 'Using Donations') {
                return `${this.recipient.name}이(가) $${trail.info.amount}을(를) ${trail.info.name}에서  ${trail.info.message}을(를) ${trail.info.purpose}하는데 사용`;
            }
        },
        donate() {
            if (this.recipient.donation_progress === 100) {
                alert('Donation Completed');
                return;
            }
            movePage(`donation.html?wallet=${this.wallet}`);
        },

    }
});
