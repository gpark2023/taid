var app = new Vue({
    el: '#app',
    data: {
        shop: null
    },
    mounted() {
        let shopName = getParameterByName('shopName');
        console.log('shopName', shopName);
        this.fetchShopDetail(shopName);
    },
    methods: {
        async fetchShopDetail(shopName) {
            try {
                if (!shopName) {
                    return false;
                }
                const response = await axios.get(`http://taid.kr/view/shop/${shopName}`);
                console.log(response);
                this.shop = response.data;
            } catch (error) {
                console.error(error);
            }
        },
        async buypage(good, wallet) {
            let shopn = getParameterByName('shopName');
            movePage(`buy.html?wallet=${wallet}&good=${good}&shopName=${shopn}`);
        },
    }
});
