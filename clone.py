from Utils.colours import *
import Utils.git as git
import argparse , os
import Core.repositries as repositries
import Utils.checker as checker
import Core.caller as caller
import Core.profile as profile
import Core.file as file
import Core.repo_info as Repo
import Core.graph as graph
import Core.topic_repositories as topicrepositries
import Core.topic_repo_info as TopicRepo
import Core.topic_graph as tgraph
from tqdm.std import trange


# Just a fancy ass  banner
print('''%s    ____     _______ __     ________
   /  _/    / ____(_) /_   / ____/ /___  ____  ___  _____
   / /_____/ / __/ / __/  / /   / / __ \/ __ \/ _ \/ ___/
 %s_/ /_____/ /_/ / / /_   / /___/ / /_/ / / / /  __/ /
%s/___/     \____/_/\__/   \____/_/\____/_/ /_/\___/_/   %sv1.0.0%s\n''' %
      (red , red ,red ,  green, white))

print('''%s+-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+-+-+-+-+-+
|                Developer: Sarvesh Kumar Dwivedi               |
+-+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+ +-+-+-+-+-+ +-+-+-+-+-+-+-+%s'''%(yellow , white))


def Options():
      # Processing command line arguments
      parser = argparse.ArgumentParser()
      # Options
      parser.add_argument('-n', '--names', help='name of the account with git repositry', dest='name')
      parser.add_argument('-g', '--graph', help='graph format (default bar)', dest='graph', choices=['pie', 'bar'])
      parser.add_argument('-o', '--output', help='cloning path', dest='output')
      parser.add_argument('-t', '--topics', help='topics to search', dest='topic')
      parser.add_argument('-trl','--rep_limit' , help='topic search repository limit (default 30)', dest='topic_rep_limit')
      parser.add_argument('--stats', help='stats of particular profile.', dest='stats' ,action='store_true' )
      parser.add_argument('--onlystats', help='only stats of a profile.', dest='onlystats' ,action='store_true' )
      # parser.add_argument('--update', help='update I-Git-Cloner', dest='update',action='store_true')
      parser.add_argument('--wayback', help='fetch profiles from searched topic repositries', action='store_true')
      args = parser.parse_args()
      if args.name == None and args.topic == None:
            print('\n' + parser.format_help().lower())
            return [False]
      else:
            return [True , args]

def get_output_dir(args):
      # If the user has supplied --output argument
      if args.output != None:
            if os.path.exists(args.output):
                  output_dir = args.output
            else:
                  print(f"path {args.output} does not exists.")
                  quit()
      else:
            output_dir = os.curdir

      return output_dir



def get_name(repos, link):
    for key, value in repos.items():
         if link == value:
             return key
      

def get_graph_format(args):
      graph_type = ''
      if bool(args.graph):
            if args.graph == 'pie':
                  graph_type = 'pie'
            else:
                  graph_type = 'bar'
      else:
            graph_type = 'bar'
      return graph_type

def get_topic_rep_limit(args):
      topic_rep_limit = 30
      if bool(args.topic_rep_limit):
            try:
                  topic_rep_limit = int(args.topic_rep_limit)
            except:
                  pass
      return topic_rep_limit


def profile_stuff(names , output_dir , options):
      for name in names:
            username_directory = os.path.join(output_dir , name)
            print_info(yellow , f"[!] Scanning for username {name}. \n Searching.... \n")
            if checker.check_profile(name):
                  print_info(green , f"username {name} found.")
                  repo_instance = repositries.Repositries(name)
                  if not options.onlystats:
                        repos = repo_instance.repositry_info
                        links = checker.print_and_get_repos(repos)
                        for link in links:
                              rep_name = get_name(repos , link)
                              print_info(yellow , f'Cloning {rep_name}')
                              caller.clone(link , os.path.join(username_directory , rep_name))
                              print_info(green , f"Cloned {rep_name} in directory {os.path.join(username_directory , rep_name)}. \n")

                  if options.stats or options.onlystats:
                        username_stats_directory = os.path.join(output_dir , 'stats ' + name)
                        print_info(yellow , f"Generating stats for username {name}.")
                        profile_instance = profile.Profile(name)
                        profile_info = profile_instance.info
                        file.MakeFile(profile_info , username_stats_directory , 'profile')
                        repos = repo_instance.repositry_list

                        for i in trange(len(repos)):
                              repo = repos[i]
                              repo_info_instance = Repo.RepoInfo(repo)
                              repo_info = repo_info_instance.info
                              file.MakeFile(repo_info , username_stats_directory , 'repositories')

                        print_info(blue , f"Generating Graphs.")
                        graph_format = get_graph_format(options)
                        graph.Graph(username_stats_directory , graph_format)
                        print_info(green , f"Generated Graphs.")
                        print()
                        print_info(green , f"Generated stats for username {name} in directory {username_stats_directory}.")


            else:
                  print_info(red , f"username {name} does not exists.")

def topic_stuff(topics , output_dir , options):
      for topic in topics:
            topic_directory = os.path.join(output_dir , topic)
            print_info(yellow , f"[!] Scanning for topic {topic}. \n Searching.... \n")
            if checker.check_topic(topic):
                  print_info(green , f"Topic {topic} found.")
                  topic_rep_limit = get_topic_rep_limit(options)
                  repo_instance = topicrepositries.Repositries(topic , limit=topic_rep_limit)
                  if not options.onlystats:
                        repos = repo_instance.repositry_info
                        links = checker.print_and_get_repos(repos)
                        for link in links:
                              name = get_name(repos , link)
                              print_info(yellow , f'Cloning {name}')
                              caller.clone(link , topic_directory)
                              print_info(green , f"Cloned {name} in directory {topic_directory}. \n")

                  if options.stats or options.onlystats:
                        topic_stats_directory = os.path.join(output_dir , 'stats ' + topic)
                        print_info(yellow , f"Generating stats for topic {topic}.")
                        repos = repo_instance.repositry_info
                        

                        for repo in repos:
                              link = repos[repo]
                              name = get_name(repos , link)
                              repo_info_instance = TopicRepo.TopicRepoInfo(link , name)
                              repo_info = repo_info_instance.info
                              file.MakeFile(repo_info , topic_stats_directory , 'repositories')

                        # Checking for wayback argument.
                        if options.wayback:
                              top_profiles = list(repo_instance.profiles)
                              for prof in top_profiles:
                                    profile_instance = profile.Profile(prof)
                                    profile_info = profile_instance.info
                                    file.MakeFile(profile_info , topic_stats_directory , 'profile')

                        print_info(blue , f"Generating Graphs.")
                        graph_format = get_graph_format(options)
                        tgraph.TGraph(topic_stats_directory , graph_format)
                        print_info(green , f"Generated Graphs.")
                        print()
                        print_info(green , f"Generated stats for username {topic} in directory {topic_stats_directory}.")
            else:
                  print_info(red , f"Sorry unable to search topic {topic}.")



# s0md3v , khuyentran1401
if __name__ == '__main__':
      if git.is_tool():
            option = Options()
            if option[0]:
                  options = option[1]
                  output_dir = get_output_dir(options)
                  if bool(options.name):
                        names = options.name.split(",")
                        profile_stuff(names , output_dir , options)
                  if bool(options.topic):
                        topics = options.topic.split(",")
                        topic_stuff(topics , output_dir , options)
      else:
            print_info(red , "please install git in order to continue.")
            
             