export default {
  async fetch(request) {
    const url = new URL(request.url);
    const PREFIX = '/blog/ai-buzzwords';
    const newPath = url.pathname.slice(PREFIX.length) || '/';
    return fetch(`https://ai-buzzwords.pages.dev${newPath}${url.search}`, {
      headers: request.headers,
    });
  },
};
