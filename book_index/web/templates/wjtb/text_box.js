Vue.component('text-box', {
    template : `{% include 'wjtb/text_box.html' %}`,

    created() {
        var self = this;
    },

    data: () => ({
        selected_page_text: null,
        image_url: null,
        predicted_level: 0
    }),

    methods: {

        predict_text: function(){

              var f_self = this;

              axios.request({
                method: 'post',
                url: './predict_text',
                data: {
                        'page_text': f_self.selected_page_text
                    },
                headers: {
                    'Content-Type': 'application/json'
                },
              })

              .then((response) => {

                  var level = response.data.level;
                  self.predicted_level.innerHTML = JSON.stringify(level, null, 4);

               })

              .catch((err) => {
                  alert('파일 전송에 실패했습니다.');
            })

        },

    }
});
