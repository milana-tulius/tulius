import thread_actions from '../components/thread_actions.js'
import online_status from '../components/online_status.js'
import comments_component from '../../forum/components/comments.js'
import reply_form_component from '../../forum/components/reply_form.js'


export default LazyComponent('gameforum_thread_page', {
    template: '/static/gameforum/pages/thread.html',
    data: function () {
        return {
            breadcrumbs: [],
            loading: true,
            thread: {online_ids: [], id: null},
            comments_page: 1,
        }
    },
    computed: {
        user: function() {return this.$root.user;},
        variation: function() {return this.$parent.variation},
    },
    methods: {
        load_api(pk, page) {
            this.comments_page = page;
            if (this.thread.id == pk)
                return;
            this.$root.loading_start();
            axios.get(
                '/api/game_forum/variation/'+ this.variation.id + '/thread/' + pk + '/'
            ).then(response => {
                this.thread = response.data;
                this.breadcrumbs = []
                for (var item of this.thread.parents)
                    this.breadcrumbs.push(
                        {"url": item.url, "title": item.title});
                this.breadcrumbs.push(
                    {"url": this.thread.url, "title": this.thread.title});
                this.loading = false;
            }).catch(error => this.$root.add_message(error, "error"))
            .then(() => {
                this.$parent.loading_end(this.breadcrumbs);
            });
        },
        mark_all_not_readed() {
            axios.delete('/api/game_forum/variation/'+ this.variation.id + '/thread/'+ this.thread.id + '/read_mark/').then(response => {
                this.thread.last_read_id = response.data.last_read_id;
                this.thread.not_read_comment = response.data.not_read_comment;
            }).catch(error => this.$parent.add_message(error, "error"));
        },
    },
    mounted() {
        this.load_api(this.$route.params.id, this.$route.query['page'] || 1)
    },
    beforeRouteUpdate (to, from, next) {
        this.load_api(to.params.id, to.query['page'] || 1);
        next();
    },
})
