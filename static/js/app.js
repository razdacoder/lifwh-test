const burger = document.querySelector('.burger')
const nav = document.querySelector('.responsive')
const close = document.querySelector('.close')
if (burger) {
    burger.addEventListener('click', () => {
        nav.style.display = 'block';
        nav.style.right = '0';
    })

    close.addEventListener('click', () => {
        nav.style.right = '-52%';
        nav.style.display = 'none';
        
    })
    
}