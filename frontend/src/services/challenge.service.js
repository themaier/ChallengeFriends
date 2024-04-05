import axios from 'axios';

const ipv4 = import.meta.env.VITE_IPV4 || 'localhost';
const API_URL = `http://${ipv4}:8000/challenges/`;

class ChallengeService {

    async createChallenge(challenge) {
        return await axios.post(API_URL, challenge).then(response => {
            return response
        })
    }

    async getPendingChallenges(id) {
        return await axios.get(API_URL + id + '/pending').then(response => {
            return response
        })
    }

    async getAcceptedChallenges(id) {
        return await axios.get(API_URL + id + '/accepted').then(response => {
            return response
        })
    }
    
    async getCreatedChallenges(id) {
        return await axios.get(API_URL + id + '/created').then(response => {
            return response
        })
    }

    async acceptChallenge(id) {
        return await axios.put(API_URL + id + '/accept').then(response => {
            return response
        })
    }

    async declineChallenge(id) {
        return await axios.put(API_URL + id + '/decline').then(response => {
            return response
        })
    }

    async getCompletedChallengesByUser(id, userId) {
        return await axios.get(API_URL + id + '/done?logged_in_user_id=' + userId).then(response => {
            return response
        })
    }

    async getCompletedChallengesByTag(hashtag, id) {
        return await axios.get(API_URL + hashtag + '?userId=' + id).then(response => {
            return response
        })
    }

    async getTrendingChallenges(id) {
        return await axios.get(API_URL + 'latest/' + 10 + '?userId=' + id).then(response => {
            return response
        })
    }

    async likeChallenge(challengeId, userId) {
        return await axios.put(API_URL + challengeId + '/like', {
            user_id: userId,
            challenge_id: challengeId
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
        }).then(response => {
            return response
        })
    }
};

export default new ChallengeService();