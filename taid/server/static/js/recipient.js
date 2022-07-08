var app = new Vue({
    el: '#app',
    data: {
        recipients: [],
    },
    mounted() {
        this.fetchRecipients();
    },
    methods: {
        async fetchRecipients() {
            try {
                const response = await axios.get('http://taid.kr/view/all_recipient');
                this.recipients = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        showDetail(wallet) {
            movePage(`recipient_detail.html?wallet=${wallet}`);
        }
    }
});
