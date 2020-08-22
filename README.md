# mosh_scrap

Little python script that uses BeautifulSoup to download all videos and files related to a specified course at https://codewithmosh.com/.

You need to be logged in at https://codewithmosh.com/ (in your browser) and had access to a specified course.

To use it just run it with required arguments:
    
    python main.py https://codewithmosh.com/courses/enrolled/417695 -f
    
    Required arg0: "course_url" eg.:https://codewithmosh.com/courses/enrolled/417695.
    
    Required arg1: "used_browser" from which we will copy the cookies with login info.
    For now you can use "-f" as firefox or "-c" as chrome.
    
It will create new "download" drectory next to main.py, with seperate subfolders for each section of the course.

I personally checked it with these courses:
    
    * Complete Python Mastery
    * The Ultimate Design Patterns: Part 1
    * The Ultimate Design Patterns: Part 2
    * The Ultimate Data Structures & Algorithms: Part 1
    * The Ultimate Data Structures & Algorithms: Part 2
    * The Ultimate Data Structures & Algorithms: Part 3
