import axios from 'axios';
import https from 'https'

const ipv4 = import.meta.env.VITE_IPV4 || 'http://localhost:8000';
const API_URL = `${ipv4}/challenges/`;
const httpsAgent = new https.Agent({ rejectUnauthorized: false });
const config = API_URL.startsWith('https://') ? { httpsAgent } : {};

class ChallengeService {

    async createChallenge(challenge) {
        return await axios.post(API_URL, challenge, config).then(response => {
            return response
        })
    }

    async getPendingChallenges(id) {
        return await axios.get(API_URL + id + '/pending', config).then(response => {
            return response
        })
    }

    async getAcceptedChallenges(id) {
        return await axios.get(API_URL + id + '/accepted', config).then(response => {
            return response
        })
    }
    
    async getCreatedChallenges(id) {
        return await axios.get(API_URL + id + '/created', config).then(response => {
            return response
        })
    }

    async acceptChallenge(id) {
        return await axios.put(API_URL + id + '/accept', config).then(response => {
            return response
        })
    }

    async declineChallenge(id) {
        return await axios.put(API_URL + id + '/decline', config).then(response => {
            return response
        })
    }

    async getCompletedChallengesByUser(id, userId) {
        return await axios.get(API_URL + id + '/done?logged_in_user_id=' + userId, config).then(response => {
            return response
        })
    }

    async getCompletedChallengesByTag(hashtag, id) {
        return await axios.get(API_URL + hashtag + '?userId=' + id, config).then(response => {
            return response
        })
    }

    async getTrendingChallenges(id) {
        return await axios.get(API_URL + 'latest/' + 10 + '?userId=' + id, config).then(response => {
            return response
        })
    }

    async likeChallenge(challengeId, userId) {
        return await axios.put(API_URL + challengeId + '/like', {
            user_id: userId,
            challenge_id: challengeId,
            config
        }).then(response => {
            return response
        })
    }

    async completeChallenge(challengeId, image) {
        const formData = new FormData();
        formData.append('image', image);
        
        return await axios.put(`${API_URL}${challengeId}/done`, formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            },
            config
        }).then(response => {
            return response
        })
    }

    async addComment(challengeId, userId, comment, image) {
        const formData = new FormData();
        if(image != null) {
            formData.append('image', image);
        }
        if(comment != null && comment != "") {
            formData.append('comment_text', comment);
        };
        formData.append('user_id', userId);
        return await axios.put(`${API_URL}${challengeId}/comment`, formData, {
            headers: {
            'Content-Type': 'multipart/form-data',
            },
            config
        }).then(response => {
            return response
        })
    }
};

export default new ChallengeService();