import axios from 'axios'

const ipv4 = import.meta.env.VITE_IPV4 || 'localhost';
const API_URL = `http://${ipv4}:8000/users/`

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