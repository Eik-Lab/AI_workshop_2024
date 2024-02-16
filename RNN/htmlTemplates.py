css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://scontent-arn2-1.xx.fbcdn.net/v/t31.18172-8/15016377_1267657659923132_5791758166595430008_o.jpg?_nc_cat=105&ccb=1-7&_nc_sid=7a1959&_nc_ohc=Doii1_UEQRIAX_1dboq&_nc_ht=scontent-arn2-1.xx&oh=00_AfB06VnbUiLOX4Cb849U4BHFSEFmb8ScdVBrRqrMDdAG4g&oe=65F5B9D4">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://scontent-arn2-1.xx.fbcdn.net/v/t1.18169-9/10451652_395614293932952_1756426720818879979_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=7a1959&_nc_ohc=y4HCSWHwtoQAX9vWzqB&_nc_ht=scontent-arn2-1.xx&oh=00_AfCPje968OOHy9spKpYJUFzOgXZzOhorncmRp01KkDqmrQ&oe=65F5BD77">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
