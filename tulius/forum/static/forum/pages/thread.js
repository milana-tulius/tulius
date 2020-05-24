import thread_actions from '../snippets/thread_actions.js'
import online_status from '../snippets/online_status.js'
import comment_component from '../snippets/comment.js'
import pagination_component from '../components/pagination.js'
import reply_form_component from '../components/reply_form.js'


export default LazyComponent('forum_thread_page', {
    template: '/static/forum/pages/thread.html',
    data: function () {
        return {
            breadcrumbs: [],
            loading: true,
            thread: {online_ids: [], id: null},
            comments: [],
            pagination: {},
            comments_page: 1,
            user: {},
            mark_read_func: null,
            mark_read_id: null,
        }
    },
    methods: {
        subscribe_comments() {
            if (this.thread.id)
                this.$root.$socket.sendObj({action: 'subscribe_comments', id: this.thread.id});
        },
        unsubscribe_comments() {
            if (this.thread.id) {
                this.$root.$socket.sendObj({action: 'unsubscribe_comments', id: this.thread.id})
            }
            delete this.$options.sockets.onmessage
        },
        websock_message(msg) {
            var data = JSON.parse(msg.data);
            if ((data['.namespaced'] != 'thread_comments') || (data.thread_id != this.thread.id)) return;
            if (data.page > this.pagination.pages_count) {
                this.pagination.pages_count = this.pagination.pages_count + 1;
                this.pagination.pages.push(this.pagination.pages_count);
                this.pagination.is_paginated = true;
            }
            if (data.page != this.comments_page)
                return;
            axios.get('/api/forum/comment/'+ data.comment_id + '/').then(response => {
                var new_comment = response.data;
                new_comment.is_liked = false;
                var comment;
                for (comment of this.comments)
                    if (comment.id == new_comment.id)
                        return;
                this.comments.push(new_comment);
            }).catch(error => this.$parent.add_message(error, "error")).then(() => {});
        },
        fast_reply(comment) {
            var component;
            for (component of this.$refs.comments) {
                if (component.comment.id == comment.id) {
                    var el = this.$refs.reply_form.$el;
                    el.parentNode.removeChild(el);
                    component.$el.parentNode.appendChild(el);
                    break;
                }
            }
            this.$refs.reply_form.fast_reply(comment);
        },
        update_likes() {
            var comment;
            var comment_ids = []
            for (comment of this.comments)
                comment_ids.push(comment.id);
            if (!this.user.is_anonymous) {
                axios.get('/api/forum/likes/', {params: {ids: comment_ids.join(',')}}
                ).then(response => {
                    for (comment of this.comments)
                        comment.is_liked = response.data[comment.id];
                }).catch(error => this.$parent.add_message(error, "error"));
            }
        },
        set_new_comments(comments) {
            var comment;
            for (comment of comments)
                comment.is_liked = null;
            this.comments = comments;
            this.update_likes();
        },
        update_comments() {
            this.loading = true;
            this.$parent.loading_start();
            axios.get('/api/forum/thread/'+ this.thread.id + '/comments_page/' + this.comments_page + '/').then(response => {
                this.set_new_comments(response.data.comments);
                this.$options.sockets.onmessage = this.websock_message;
                this.subscribe_comments();
                this.pagination = response.data.pagination;
            }).catch(error => this.$parent.add_message(error, "error")).then(() => {
                this.loading = false;
                this.$parent.loading_end(this.breadcrumbs);
            });
        },
        load_api(pk, page) {
            this.comments_page = page;
            if (this.thread.id == pk) {
                this.update_comments();
                return;
            }
            this.unsubscribe_comments();
            this.$parent.loading_start();
            axios.get('/api/forum/thread/'+ pk).then(response => {
                const api_response = response.data;
                this.breadcrumbs = [{"url": "/forums/", "title": "Форумы"}]
                api_response.parents.forEach(
                    (item, i, arr) => this.breadcrumbs.push(
                        {"url": item.url, "title": item.title}
                    ));
                this.breadcrumbs.push(
                    {"url": api_response.url, "title": api_response.title});
                api_response.online_ids = this.thread.online_ids;
                this.thread = api_response;
                this.user = this.$parent.user;
                this.update_comments()
            }).catch(error => this.$parent.add_message(error, "error"))
            .then(() => {
                this.$parent.loading_end(this.breadcrumbs);
            });
        },
        cleanup_reply_form() {
            var form = this.$refs.reply_form;
            if (form === undefined) return;
            var el = form.$el;
            form.cleanup_reply_form();
            el.parentNode.removeChild(el);
            this.$refs.reply_form_parking.appendChild(el);
        },
        mark_as_read(comment_id) {
            if (comment_id <= this.thread.last_read_id)
                return;
            if (this.mark_read_id)
                return;
            // console.log('поставили таймер')
            this.mark_read_id = comment_id;
            this.mark_read_func = setTimeout(this.do_mark_mark_as_read, 1000, comment_id);
        },
        cancel_mark_as_read(comment_id) {
            if (this.mark_read_id == comment_id) {
                // console.log('отменили таймер');
                clearTimeout(this.mark_read_func);
                this.mark_read_id = null;
            }
        },
        do_mark_mark_as_read(comment_id) {
            // console.log('пошел запрос');
            axios.post('/api/forum/thread/'+ this.thread.id + '/read_mark/', {'comment_id': comment_id}).then(response => {
                this.thread.last_read_id = response.data.last_read_id;
            }).catch(error => this.$parent.add_message(error, "error")).then(() => {
                this.mark_read_id = null;
                this.mark_read_func = null;
            });
        }
    },
    mounted() {
        this.$options.sockets.onopen = this.subscribe_comments;
        this.load_api(this.$route.params.id, this.$route.query['page'] || 1)
    },
    beforeRouteUpdate (to, from, next) {
        this.cleanup_reply_form();
        this.load_api(to.params.id, to.query['page'] || 1);
        next();
    },
    beforeDestroy() {
        this.unsubscribe_comments();
    },
})
