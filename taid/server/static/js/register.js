
var app = new Vue({
    el: '#app',
    data: {
        type: '',
        name: '',
        id: '',
        pwd: '',
        anonymity: '1',
        residence: '',
        region: '',
        goods: [{
            name: '',
            price: ''
        }],
        age: '',
        neededItem: '',
        story: '',
        purpose: '',
        amountNeeded: '',
        pictureFile: null
    },
    methods: {
        async validate() {
            if (!this.type) {
                alert('select a type');
                return false;
            } else if (!this.name) {
                alert('input a name');
                return false;
            } else if (!this.id) {
                alert('input an ID');
                return false;
            } else if (!this.pwd) {
                alert('input an password');
                return false;
            }

            let type = parseInt(this.type);
            switch(type) {
                case 2:
                    if (!this.residence) {
                        alert('input a residence');
                        return false;
                    }
                    break;
                case 3:
                    if (!this.region) {
                        alert('input a region');
                        return false;
                    }
                    if (!this.makeGoodsParameter()) {
                        return false;
                    }
                    break;
            }

            return true;
        },
        makeGoodsParameter() {
            let params = {};
            for (let i = 0; i < this.goods.length; i++) {
                if (!this.goods[i].name && !this.goods[i].price) {
                    continue;
                }

                if (!this.goods[i].name) {
                    alert('Input a name');
                    return false;
                }

                if (!this.goods[i].price) {
                    alert('Input a price');
                    return false;
                }

                params[this.goods[i].name] = this.goods[i].price;
            }
            return params;
        },
        async register() {
            try {
                if (!(await this.validate())) {
                    return false;
                }

                let params = {
                    type: parseInt(this.type),
                    name: this.name,
                    id: this.id,
                    pw: this.pwd,
                };

                let type = parseInt(this.type);
                switch(type) {
                    case 1:
                        params['anonymity'] = this.anonymity;
                        break;
                    case 2:
                        params['residence'] = this.residence;
                        params['age'] = this.age;
                        params['story'] = this.story;
                        //await axios.post('http://127.0.0.1:1000/transactions/new', params);
                        break;
                    case 3:
                        params['region'] = this.region;
                        params['goods'] = this.makeGoodsParameter();
                        break;
                }

                const response = await axios.post('http://taid.kr/register', params);
                if(type == 2){
                    let donate_req = {
                        purpose : "Donation Request",
                        message : this.neededItem + " at " + this.purpose,
                        recipient : "0",
                        sender : response.data,
                        amount : this.amountNeeded
                    };

                    axios.post('http://3.101.138.234:1000/transactions/new', donate_req);
                }
                alert("Your Wallet Address : " + response.data);
                movePage('recipient.html');
            } catch(error) {
                console.error(error);
            }
        },
        addGoods() {
            this.goods.push({
                name: '',
                price: ''
            });
        },
        removeGoods(index) {
            this.goods.splice(index, 1);
        }
    }

});
