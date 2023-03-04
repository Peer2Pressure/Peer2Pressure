import Cookies from 'js-cookie';

export default function getCsrfToken() {
    const csrftoken = Cookies.get('csrftoken');
    return csrftoken;
  }