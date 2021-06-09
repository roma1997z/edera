class AddUser extends React.Component{
    constructor(props) {
        super(props);
        this.state={users:this.props.users,
                    pairs:this.props.pairs,
                    chats:this.props.chats,
                    add_user:{modal:false, user_id:0},
                    add_pair:{student:0, teacher:0},
                    add_chat:{pair:{id:0}, chat:{id:0}},
                    add_lesson:{pair_id:0, date:0}
        };
        console.log(this.state.chats);
    }

    add_user(role="student"){
        var name = prompt("Please enter " + role + " name", "Mark Ivanov");
        if(name!=null){
            var formData = new FormData();
            formData.append("csrfmiddlewaretoken", this.props.token);
            formData.append("name", name);
            formData.append("role", role);
            formData.append("add_user", 1);
            fetch("", {method: "POST", body: formData}).then(response => response.json()).then((resp) => {
                console.log(resp);
                var users = this.state.users.slice();
                users.push(resp.user)
                this.setState({users:users})
                });
        }
    }

    add_pair(){
        console.log(this.state.add_pair);
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", this.props.token);
        formData.append("user_id", this.state.add_pair.student);
        formData.append("teacher", this.state.add_pair.teacher);
        formData.append("add_pair", 1);
        fetch("", {method: "POST", body: formData}).then(response => response.json()).then((resp) => {
                console.log(resp)
                var pairs = this.state.pairs.slice()
                if(resp.ok){pairs.push(resp.pair);}
                this.setState({add_pair:{student:0, teacher:0}, pairs:pairs});
            });
    }

    add_chat(){
        console.log(this.state.add_chat);
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", this.props.token);
        formData.append("pair_id", this.state.add_chat.pair.id);
        formData.append("chat_id", this.state.add_chat.chat.id);
        formData.append("add_chat", 1);
        fetch("", {method: "POST", body: formData}).then(response => response.json()).then((resp) => {
                console.log(resp);
                if (resp.ok) {
                    var pairs = this.state.pairs.slice();
                    var pair_id = this.state.add_chat.pair.id
                    var index = pairs.findIndex(function(el){return el.pair_id===pair_id})
                    pairs[index]= resp.chat_id;
                    var chats = this.state.chats.slice();
                    chats.splice(this.state.add_chat.chat.index, 1)
                    this.setState({add_chat: {pair: {id: 0}, chat: {id: 0}}, pairs: pairs, chats: chats});
                }
            }
        )
    }

    pair_id_info(pair_id){
        var formData = new FormData();
        formData.append("csrfmiddlewaretoken", this.props.token);
        formData.append("pair_id_info", pair_id);
        fetch("", {method: "POST", body: formData}).then(response => response.json()).then((resp) => {
                console.log(resp);
                this.setState({add_lesson:{pair_id:pair_id, info:resp.info, old_info:resp.old_info}})})
    }
    add_lesson(){
        var formData = new FormData(document.getElementById("add_lesson"))
        formData.append("csrfmiddlewaretoken", this.props.token);
        formData.append("pair_id", this.state.add_lesson.pair_id);
        formData.append("add_lesson", 1);
        fetch("", {method: "POST", body: formData}).then(response => response.json()).then((resp) => {
                console.log(resp);
                this.setState({add_lesson:{pair_id:this.state.add_lesson.pair_id, info:resp.info, old_info: this.state.add_lesson.old_info}})
        })
    }

    cancel_lesson(lesson_id){
        var confirm = prompt("Для подтверждения введите: yes", "no")
        if(confirm=== "yes"){
            var formData = new FormData(document.getElementById("add_lesson"))
            formData.append("csrfmiddlewaretoken", this.props.token);
            formData.append("cancel_lesson", lesson_id);
            fetch("", {method: "POST", body: formData}).then(response => response.json()).then((resp) => {
                    console.log(resp);
                    this.setState({add_lesson:{pair_id:this.state.add_lesson.pair_id, info:resp.info, old_info: this.state.add_lesson.old_info}})
            });
        }
    }

    render(){
    return (
        <div className="container">
            <h2>Добавить урок для пары учитель ученик</h2>
            <div className="row">
                    {this.state.pairs.map((pair, index)=>
                        <div className="col-md-3">
                        <div className={pair.pair_id===this.state.add_lesson.pair_id?"element-card selected":"element-card"}
                        onClick={()=>this.pair_id_info(pair.pair_id)}>{pair.name}
                            {pair.chat_id ? "": <span> &#10007;</span>}</div></div>
                    )}

            </div>
            <br/>
            {this.state.add_lesson.pair_id ?
                <form id="add_lesson">
                    <div className="form-group row my-1">
                        <div className="col-md-4 col-sm-5 col-12 mb-3">
                    <input className="form-control form-control-lg mx-1" name="date" type="date" defaultValue={this.props.today}/></div>
                        <div className="col-md-4 col-sm-3 col-6 mb-3">
                            <input className="form-control form-control-lg mx-1" name="time" defaultValue="19:00"/></div>
                        <div className="col-md-4 col-sm-4 col-6  mb-3">
                        <select name="duration" className="form-control form-control-lg mx-1" defaultValue="60">
                            <option value="30">30 мин</option>
                            <option value="45">45 мин</option>
                            <option value="60">1 час</option>
                            <option value="90">1.5 часа</option>
                            <option value="120">2 часа</option>
                        </select></div>
                        <div className="col-md-4 col-sm-6 col-12 mb-3">
                            <input name="name" className="form-control form-control-lg mx-1" defaultValue="Mathematics"/>
                        </div>
                        <div className="col-md-4 col-sm-6 col-6 mb-3">
                            <select name="repeat" className="form-control form-control-lg mx-1" defaultValue="0">
                                <option value="0">Одноразовый</option><option value="1">Повторяющийся</option></select>
                            </div>
                        <div className="col-md-4 col-sm-6 col-6 mb-3">
                    <button type="button" className="btn btn-lg btn-success mx-1"
                            onClick={()=>this.add_lesson()}>Добавить урок</button></div>
                    </div>

                    <div>
                        <table className="table table-striped">
                            <thead>
                            <tr><th>Текст</th><th>Повтор</th><th>Уведомление<br/> отправлено</th><th>Удалить</th></tr>
                            </thead>
                            <tbody>
                            {this.state.add_lesson.info.map((el, index)=>
                            <tr><td>{el.start} - {el.end} {el.name}</td>
                                <td>{el.repeat ? <span>&#10003;</span> : ""}</td>
                                <td>{el.notification ? <span>&#10003;</span> :""}</td>
                                <td className="click" onClick={()=>this.cancel_lesson(el.id)}><strong className="text-danger">Отменить</strong></td>
                            </tr>
                            )}
                            </tbody>
                        </table>
                        <strong>Текст для копирования</strong>
                        {this.state.add_lesson.old_info.map((el, index)=>
                            <p className="text-success">{el.start} - {el.end} {el.name} ({el.teacher}) </p>)}
                        {this.state.add_lesson.info.map((el, index)=>
                            <p>{el.start} - {el.end} {el.name} ({el.teacher}) </p>)}
                    </div>
                </form>:<p>Выберите пару ученик-учитель</p>
            }
            <br/>
            <hr/>
            <div className="row">
                <div className="col-md-6">
                    <h2>Ученики</h2>
                     {this.state.users.filter(function (user) {return user.role === "student"}).map((user, index)=>
                     <div className={user.user_id===this.state.add_pair.student?"element-card selected":"element-card"}
                          onClick={()=>this.setState({add_pair:{student:user.user_id, teacher:this.state.add_pair.teacher}})}>{user.name}</div>)
                     }
                     <div className="element-card" onClick={()=>this.add_user("student")}><span className="text-success">Добавить ученика</span></div>
                </div>
                <div className="col-md-6">
                    <h2>Учителя</h2>
                    {this.state.users.filter(function (user) {return user.role === "teacher"}).map((user, index)=>
                     <div className={user.user_id===this.state.add_pair.teacher?"element-card selected":"element-card"}
                          onClick={()=>this.setState({add_pair:{student:this.state.add_pair.student, teacher:user.user_id}})}>{user.name}</div>)
                     }
                     <div className="element-card" onClick={()=>this.add_user("teacher")}><span className="text-success">Добавить учителя</span></div>
                </div>
            </div>
            <div>
                <p>Чтобы добавить пару выберите ученика из левой колонки, учитель из правой и нажмите создать пару.</p>
                <button type="button" className="btn btn-success" onClick={()=>this.add_pair()}
                        disabled={!this.state.add_pair.student || !this.state.add_pair.teacher}>Создать пару ученик-учитель</button>
            </div>
                <br/>
            <hr/>
            <div className="row">
                <div className="col-md-6">
                   <h2>Пары учитель-ученик без чата</h2>
                    {this.state.pairs.filter(function (pair) {return pair.chat_id === 0}).map((pair, index)=>
                        <div className={pair.pair_id===this.state.add_chat.pair.id?"element-card selected":"element-card"}
                        onClick={()=>this.setState({add_chat:{pair:{id:pair.pair_id, index:index}, chat:this.state.add_chat.chat}})}>{pair.name}</div>
                    )}
                </div>
                <div className="col-md-6">
                   <h2>Чаты с ботом без пары</h2>
                    {this.state.chats.map((chat, index)=>
                        <div className={chat.chat_id===this.state.add_chat.chat.id?"element-card selected":"element-card"}
                        onClick={()=>this.setState({add_chat:{pair:this.state.add_chat.pair, chat:{id:chat.chat_id, index:index}}})}><span>{chat.text} ({chat.date})</span><br/><small>{chat.chat_id}</small></div>
                    )}
                    <p>Чтобы добавить групповой чат:<br/>
                    <ul><li>Добавьте @Edera_bot в групповой чат</li>
                        <li>Дайте боту права администратора</li>
                        <li>Напишите любое сообщение в чат</li>
                        <li>Обновите страницу, чат появится здесь</li>
                    </ul>
                    </p>
                </div>
            </div>
            <button type="button" className="btn btn-success" onClick={()=>this.add_chat()}
            disabled={!this.state.add_chat.pair.id || !this.state.add_chat.chat.id}
            >Связать пару и чат</button>
            <br/>
            <hr/>

        </div>
    )
    }
}
