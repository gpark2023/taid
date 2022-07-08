var app = new Vue({
    el: '#app',
    data: {
        shops: [],
    },
    mounted() {
        this.fetchShops();
    },
    methods: {
        async fetchShops() {
            try {
                const response = await axios.get('http://taid.kr/view/all_shops');
                this.shops = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        viewShopDetail(shopName) {
            movePage(`shop_detail.html?shopName=${shopName}`);
        }
    }
});
