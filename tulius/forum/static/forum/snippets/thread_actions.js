import thread_access from '../components/thread_access.js'
import edit_room from '../components/edit_room.js'


export default LazyComponent('forum_thread_actions', {
    template: '/static/forum/snippets/thread_actions.html',
    props: ['thread'],
    data: function () {
        return {
            csrftoken: getCookie('csrftoken'),
            delete_comment: '',
        }
    },
    computed: {
        user: function() {return this.$root.user;},
        urls() {return this.$parent.urls},
        delete_title: function() {
            return this.thread.room ? 'Удалить эту комнату?' : 'Удалить эту тему?';
        }
    },
    methods: {
        mark_not_readed() {
            this.$parent.mark_all_not_readed();
        },
        mark_all_as_readed() {
            this.$parent.mark_all_as_readed();
        },
        delete_thread(bvModalEvt) {
            axios.delete(this.thread.url, {params: {comment: this.delete_comment}}
            ).then(response => {
                if (this.thread.room)
                    this.$root.add_message("Комната успешно удалена", "warning");
                else
                    this.$root.add_message("Тема успешно удалена", "warning");
                if (this.thread.parents.length > 0) {
                    this.$router.push({
                        name: 'forum_room',
                        params: { id: this.thread.parents[this.thread.parents.length - 1].id }
                    })
                } else {
                    this.$router.push({ name: 'forum_root'})
                }
            }).catch(error => this.$root.add_message(error, "error"))
            .then(() => {});
        },
    }
})
