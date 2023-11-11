<template>
    <div style="width: 100%;background-color: #ffffff;">
    <div class="mainLayout">
        <div v-for="team in vTeams">
            <h1>{{team.team_name}}</h1>

            <template v-for="group in vGroups">
                <div v-if="group.team_id==team.id">
                    <h2 style="text-align: center;" v-if="ismobile">{{ group.group_name }}</h2>
                    <n-divider v-else><h2 style="text-align: center;">{{ group.group_name }}</h2></n-divider>
                    <div  class="group-content">

                    <template v-for="member in vMembers">
                        <div class="card" v-if="member.group_id==group.id">
                            <div style="display: inline-block;" class="card-p1">
                                <el-avatar :size="100" :src="member.img"/>
                            </div>
                            <div style="display: inline-block;" class="card-p2">
                                <h2 style="margin: 0;">{{member.name}}</h2>
                                <span>
                                    <br>
                                    {{ member.campus }}<br>
                                    {{ member.school }}<br>
                                </span>
                            </div>
                        </div>
                    </template>
                    </div>
                </div>
            </template>
            <el-divider v-if="ismobile"/>
        </div>
    </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            vTeams:null,
            vGroups:null,
            vMembers:null,
        }
    },
    props:['ismobile'],
    methods:{
    },
    mounted(){
        axios.get(this.$store.state.vteamAPI).then(response=>{
            this.vTeams=response.data
        }),
        axios.get(this.$store.state.vgroupAPI).then(response=>{
            this.vGroups=response.data
        }),
        axios.get(this.$store.state.vmemberAPI).then(response=>{
            this.vMembers=response.data
        })
    },
}
</script>

<style scoped>
.mainLayout{
    margin: 0 12%;
    min-height: 83vh;
    padding: 1em 0;
    background-color: #ffffff;
}
.group-content{
    display:flex;
    flex-wrap: wrap;
    justify-content: center;
}
.card{
    flex-grow: 1;
    background: linear-gradient(to bottom, #70b5ff, #3f9cfd);
    display: flex;
    justify-content: center;
    align-items: center;
    width: 350px;
    height: 150px;
    border-radius: 5px;
    margin: 0.5em;
}
.card-p1{
    padding-right: 1em;
}
.card-p2{
    width: 150px;
}

@media screen and (max-width: 800px) {
    * {
    overflow-x: hidden !important;
    overflow-y: hidden;
    word-wrap: break-word;
    overflow-wrap: break-word;
    }
    .mainLayout{
    margin: 0 1em;
    }
}
</style>