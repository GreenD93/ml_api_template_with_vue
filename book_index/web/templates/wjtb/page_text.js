Vue.component('page-text', {

    template : `{% include 'wjtb/page_text.html' %}`,

    created() {
        var self = this;
    },

    data: () => ({
        uploaded_img : null,
        imageUrl_input  : "https://file.mk.co.kr/meet/neds/2015/04/image_readtop_2015_404814_14301993671898019.jpg",
        imageUrl_output  : "https://file.mk.co.kr/meet/neds/2015/04/image_readtop_2015_404814_14301993671898019.jpg"
    }),

    methods: {

        onChangeImages(){
            const file = self.file.files[0];
            this.imageUrl_input = URL.createObjectURL(file); // Create File URL
        },

        analyze_img: function(){

            var data = new FormData();

            data.append('file', self.file.files[0]);

            axios.request({
                method: 'post',
                url: './analyze_img',
                responseType: 'blob',
                data: data
            })

            .then((response) => {
                const url = URL.createObjectURL(new Blob([response.data]));
                this.imageUrl_output = url;
            })

            .catch((err) => {
                alert('파일 전송에 실패했습니다.')
            })

        }

    }

});