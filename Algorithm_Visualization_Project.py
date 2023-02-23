import pygame 
import random
import math
import sys
pygame.init()

class DrawInformation:
    BLACK= 0,0,0
    WHITE= 255,255,255
    GREEN=0,255,0
    RED=255,0,0
    GREY=128,128,128
    GRADIENTS=[
        GREY,
        (160,160,160),
        (192,192,192)
    ]
    BACKGROUND_COLOR=WHITE

    SMALL_FONT=pygame.font.SysFont("comicsans",5)
    FONT=pygame.font.SysFont("comicsans",20)
    LARGE_FONT=pygame.font.SysFont("comicsans",25)

    SIDE_PAD=100
    TOP_PAD=150

    def __init__(self,width,height,lst):
        self.width=width
        self.height=height

        self.window=pygame.display.set_mode((width,height))
        #Display via pygame in window
        pygame.display.set_caption("Sorting Algorithm Visualization")
        #Name of the window
        self.set_list(lst)

    def set_list(self,lst):
        self.lst=lst
        self.max_val=max(lst)  #return the maximum element in the list
        self.min_val=min(lst)  #return the minimum element in the list

        self.block_width= round((self.width-self.SIDE_PAD)/len(lst))
        #Explaination: 
        # Self.width là độ dài cả khung hình window để trình chiếu 
        # Self.SIDE_PAD là padding hai bên đối với cái hình
        #Pixel-width là đang tính độ rộng của các thanh bar based on khung hình và padding
        self.block_height=math.floor((self.height-self.TOP_PAD) / (self.max_val-self.min_val))
        self.start_x=self.SIDE_PAD // 2

def draw(draw_info,algo_name,ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    #Update background color to be white
    
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))
    # Cái bên trên là toạ độ của điểm gốc controls(trên cùng góc trái)

    sorting=draw_info.FONT.render("I- Insertion Sort | B- Bubble Sort | H- Heap Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2, 75))
    #Function blit take a surface and let it onto another screen
    draw_list(draw_info)
    pygame.display.update()

    
def draw_list(draw_info,color_positions={}, clear_bg = False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
        # Đoạn này dùng để vẽ các rectangle tượng trưng trong list
        # Nãy mình có thắc mắc tại sao đoạn trên ô này tính y lại ngược như vậy thì ở đây đã có câu trả lời, ô ý đã vẽ các trục ngược xuống dưới
    
	if clear_bg:
		pygame.display.update()



def  generate_starting_list(n,min_val,max_val):
    lst=[]
    for _ in range(n):
        val= random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info , ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j],lst[j+1]=lst[j+1],lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True


def insertion_sort(draw_info, ascending=True):
    lst=draw_info.lst

    for i in range(1,len(lst)):
        current=lst[i]

        while True:
            ascending_sort = i > 0 and current < lst[i-1] and ascending
            descending_sort = i > 0 and current > lst[i-1] and not ascending 

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True


def heapify(draw_info, n, i, ascending):
    lst=draw_info.lst
    
    curr = i  
    l = 2 * i + 1 
    r = 2 * i + 2  

    if ascending:    
        if l < n and lst[curr] < lst[l]:
            curr = l
        if r < n and lst[curr] < lst[r]:
            curr = r
    if not ascending:    
        if l < n and lst[curr] > lst[l]:
            curr = l
        if r < n and lst[curr] > lst[r]:
            curr = r

    if curr != i:
        (lst[i], lst[curr]) = (lst[curr], lst[i])  # swap
        draw_list(draw_info, {i: draw_info.GREEN, curr: draw_info.RED}, True)
        heapify(draw_info, n, curr, ascending)

def heap_sort(draw_info, ascending=True):
    lst=draw_info.lst
    n = len(lst)

    for i in range(n // 2 - 1, -1, -1):
        heapify(draw_info, n, i, ascending)

    for i in range(n - 1, 0, -1):
        (lst[i], lst[0]) = (lst[0], lst[i])  # swap
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        heapify(draw_info, i, 0, ascending)
        yield True



def main():
    run=True
    clock= pygame.time.Clock()

    n=50
    min_val=0
    max_val=100

    lst=generate_starting_list(n,min_val,max_val)
    draw_info=DrawInformation(800,600,lst)
    sorting=False
    ascending=True

    sorting_algorithm = bubble_sort
    algo_name= "Bubble Sort"
    sorting_algorithm_generator=None

    while run:
        clock.tick(60)
        #Giới hạn mỗi vòng lặp sẽ chỉ chạy được 60 lần
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            #Check xem là mình có muốn quit cái game này ko(Ngang với việc ấn dấu x trên góc
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                # Nếu bạn ấn phím r thì sẽ reset lại
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting =False
            
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting= True
                sorting_algorithm_generator= sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and sorting == False:
                ascending= True
            elif event.key == pygame.K_d and sorting == False:
                ascending= False
            
            elif event.key == pygame.K_b and sorting == False:
                algo_name="Bubble Sort"
                sorting_algorithm = bubble_sort
            elif event.key == pygame.K_i and sorting == False:
                algo_name="Insertion Sort"
                sorting_algorithm = insertion_sort
            elif event.key == pygame.K_h and sorting == False:
                algo_name="Heap Sort"
                sorting_algorithm = heap_sort

    pygame.quit()

if __name__ == "__main__":
    main()





            
            