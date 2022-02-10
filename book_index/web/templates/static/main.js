var vue = new Vue({
    el: "#app",
    vuetify: new Vuetify(),

    created : function(){
    },

    data: () => ({
        menu: {
            tab:MENU_START,
            items: LIST_MENU
        }
    }),

    methods: {

        select_tab: function(tab){
            this.menu.tab = tab;
        }
    }

})