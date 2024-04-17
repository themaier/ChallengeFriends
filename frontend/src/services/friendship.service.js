import axios from 'axios'

let API_URL = import.meta.env.VITE_IPV4 || 'http://localhost:8000';
if (API_URL.startsWith("https:")) {
    API_URL = `${API_URL}/api/friendship/`;
} else {
    API_URL = `${API_URL}/friendship/`;
}

class FriendshipService {

    async addFriend(id, friendId) {
        return await axios.post(API_URL, {
            user_id: id,
            friend_user_id: friendId
        }).then(response => {
            return response
        })
    }

    async getFriends() {
        return await axios.get(API_URL).then(response => {
            return response
        })
    }

    async getFriend(id) {
        return await axios.get(API_URL + id).then(response => {
            return response
        })
    }

    async deleteFriend(user_id, friend_user_id) {
        return await axios.delete(API_URL + "?user_id=" + user_id + "&friend_user_id=" + friend_user_id).then(response => {
            return response
        })
    }
}

export default new FriendshipService();