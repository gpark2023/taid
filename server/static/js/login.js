var app = new Vue({
    el: '#app',
    data: {
        id: '',
        pwd: '',
    },
    methods: {
        async login() {
            if (!this.id) {
                alert('Invalid ID');
                return false;
            } else if (!this.pwd) {
                alert('WRONG P/W');
                return false;
            }

            try {
                const response = await axios.post('http://taid.kr/login', {
                    id: this.id,
                    pw: this.pwd,
                    type: 1
                });
                movePage('recipient.html');
            } catch (error) {
                console.error(error);
            }
        },
        async register() {
            movePage('register.html');
        }
    }
});
