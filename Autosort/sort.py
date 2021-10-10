import os 
paper_dir = './Autosort/papers_to_sort'
paper_bundles = os.listdir(paper_dir)
from pprint import pprint
import semanticscholar as sch
import datetime
import shutil
from time import mktime
import arxiv
NUM_CITATIONS_TO_KEEP = 4

def main():
    for paper in paper_bundles:
        paper_name = paper.split(' -')[0]
        paper_file_name = paper_name.lower().replace(' ','_')
        
        image_paths = os.path.join(paper_dir, paper,'assets')
        has_images = os.path.exists(image_paths)
        old_name_map = {}
        if has_images:
            if not os.path.exists(os.path.join("./Attachments/papers/",paper_file_name)):
                os.mkdir(os.path.join("./Attachments/papers/",paper_file_name))
            else:
                has_images=False # For debugging

            for i, image in enumerate(os.listdir(image_paths)):
                new_name = image.split("Image")[0]+f'_image{i}.jpg'
                old_name_map[image] = os.path.join("../../Attachments/papers/",paper_file_name,new_name)
                os.rename(os.path.join(image_paths,image), os.path.join("./Attachments/papers/",paper_file_name,new_name))
        
        with open(os.path.join(paper_dir, paper,'text.markdown')) as f:
            md_file = f.readlines()
        
        template = format_template(paper_name, md_file)
   
        if has_images:
            for i, line in enumerate(md_file):
                if '![]' == line[:3]:
                    image_path = line.split('/')[-1][:-2]
                    md_file[i] =  f"![]({old_name_map[image_path]})"

        for i, line in enumerate(md_file):
            if "[Page" in line:
                md_file[i] = line.split("(")[0]

        template = format_template(paper_name, md_file)

        with open(f'./Papers/{paper_file_name}.md', 'w') as f:
            f.write(template)

        with open('./index.md','a') as f:
            f.write(f'\n\n[[{paper_name}]] *')

        shutil.rmtree(os.path.join(paper_dir, paper))


def tuple_lists_to_string(tuple_list, line_break=False, bullets=False):
    # [(paper name, url)....]
    join_str = "\n" if line_break else "; " 
    str_list = [f"[[{title}]] {url}" for (title,url) in tuple_list]
    if bullets:
        str_list = ["* "+ x for x in str_list]
    return join_str.join(str_list)

def get_authors(authors):
    if len(authors) > 4:
        authors = authors[:3] + [authors[-1]]
    return ", ".join(map(lambda x: f"[[{x}]]", authors))

def format_template(paper_title, annotations, paper_tags=None):
    with open('./Autosort/templates/paper.md', 'r') as f:
        template = ''.join(f.readlines())

    arxiv_paper, topics, references, notable_citations = get_paper_and_citations(paper_title)
   
    if arxiv_paper:
        template = template.format(TITLE=paper_title,
                                AUTHORS= get_authors(arxiv_paper['authors']),
                                PUBURL=arxiv_paper['arxiv_url'],
                                ABSTRACT=arxiv_paper['summary_detail']['value'].replace("\n"," "),
                                DATEPUB=datetime.datetime.fromtimestamp(mktime(arxiv_paper['published_parsed'])).strftime('%d %B %Y'), # Year Published
                                DATEREAD=datetime.datetime.now().strftime('%d %B %Y'), # Date Read
                                NOTECITE=tuple_lists_to_string(notable_citations),
                                TAGS=", ".join(['#'+x for x in topics]),
                                #Body
                                ANNOTATIONS="".join(annotations),
                                #Footer
                                REFERENCES=tuple_lists_to_string(references,line_break=True,bullets=True))
    else:
        template = template.replace('{TITLE}', paper_title)
        template = template.replace('{ANNOTATIONS}', "".join(annotations))

    return template

def get_arxiv_article_id(title):
    query_results = arxiv.query(query=f"ti:{title}", max_results=5)
    
    flattened_title = title.lower().replace(" ", "")
    title_length = len(flattened_title)
    if len(query_results) > 1:
        query_results = list(filter(lambda x: x['title'].replace("\n","").lower().replace(" ", "")[:title_length]==flattened_title, query_results))
    return query_results[0] if len(query_results)>0 else None

def rank_citations_of_paper(notable_citations, cited_by):
    # Get citation counts 
    for paper in cited_by:
        if 'paperId' in paper.keys():
            paper['num_citations'] = len(sch.paper(paper['paperId'], timeout=2)['citations'])
    newlist = sorted(cited_by, key=lambda k: k['num_citations']) 

    collected_papers = [x['title'] for x in notable_citations]
    for paper in reversed(newlist):
        if paper['title'] not in collected_papers and len(notable_citations) < NUM_CITATIONS_TO_KEEP:
            notable_citations.append(paper)

    return notable_citations

def get_paper_and_citations(title):
    arxiv_article = get_arxiv_article_id(title)
    if arxiv_article is None:
        return None, None, None, None

    arxiv_id = "arXiv:" + arxiv_article['id'].split('/abs/')[-1].split('v')[0]

    sch_paper = sch.paper(arxiv_id, timeout=2)
    topics = [topic['topic'].title().replace(" ","") for topic in sch_paper['topics']]
    references = [(paper["title"], paper["url"]) for paper in sch_paper['references']]
    cited_by = sch.paper(arxiv_id, timeout=2)['citations']


    notable_citations = []
    for paper in cited_by:
        if paper['isInfluential'] and len(notable_citations) < NUM_CITATIONS_TO_KEEP:
            notable_citations.append(paper)

    if len(notable_citations) < NUM_CITATIONS_TO_KEEP:
        notable_citations = rank_citations_of_paper(notable_citations, cited_by)
    
    notable_citations = [(paper['title'], paper['url']) for paper in notable_citations]
    return arxiv_article, topics, references, notable_citations



if __name__ == "__main__":
    main()