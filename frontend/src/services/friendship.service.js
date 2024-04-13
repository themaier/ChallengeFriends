import axios from 'axios'

const ipv4 = import.meta.env.VITE_IPV4 || 'http://localhost:8000';
const API_URL = `${ipv4}/friendship/`
const config = API_URL.startsWith('https://') ? { httpsAgent } : {};

class FriendshipService {

    async addFriend(id, friendId) {
        return await axios.post(API_URL, {
            user_id: id,
            friend_user_id: friendId,
            config
        }).then(response => {
            return response
        })
    }

    async getFriends() {
        return await axios.get(API_URL, config).then(response => {
            return response
        })
    }

    async getFriend(id) {
        return await axios.get(API_URL + id, config).then(response => {
            return response
        })
    }

    async deleteFriend(user_id, friend_user_id) {
        return await axios.delete(API_URL + "?user_id=" + user_id + "&friend_user_id=" + friend_user_id, config).then(response => {
            return response
        })
    }
}

export default new FriendshipService();