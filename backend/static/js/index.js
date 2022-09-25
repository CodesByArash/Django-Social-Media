//sidebar
const menuItems=document.querySelectorAll('.menu-item');

const changeActiveItem=() =>{
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}


menuItems.forEach(item =>{
    item.addEventListener('click', () => {
        changeActiveItem();
        item.classList.add('active');
    })
})

const createbtn = document.querySelectorAll('.btn');


createbtn.forEach(item =>{
    item.addEventListener('click', () => {
        // if(item.id != 'create'){
        //     document.querySelector('.post-create')
        //     .style.display = 'none';
        // }
        if(item.id == 'create'){
            if(document.querySelector('.addpost').style.display == 'grid'){
            document.querySelector('.addpost').style.display = 'none';}
            else{
                document.querySelector('.addpost').style.display = 'grid'
            }
        }
    })
})

const closebtn = document.querySelectorAll('.closebtn');

closebtn.forEach(item =>{
    item.addEventListener('click', () => {
        if(document.querySelector('.addpost').style.display == 'grid'){
        document.querySelector('.addpost').style.display = 'none';}
    })
})

