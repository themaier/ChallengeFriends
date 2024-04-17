import axios from 'axios'

let API_URL = import.meta.env.VITE_IPV4 || 'http://localhost:8000';
if (API_URL.startsWith("https:")) {
    API_URL = `${API_URL}/api/users/`;
} else {
    API_URL = `${API_URL}/users/`;
}


class UserService {

    async register(user) {
        return await axios.post(API_URL, user).then(response => {
            return response
        })
    }

    async login(user) {
        return await axios.post(API_URL + 'verify', user).then(response => {
            return response
        })
    }

    async getUsers() {
        return await axios.get(API_URL).then(response => {
            return response
        })
    }

    async getUser(id) {
        return await axios.get(API_URL + id).then(response => {
            return response
        })
    }
}

export default new UserService();