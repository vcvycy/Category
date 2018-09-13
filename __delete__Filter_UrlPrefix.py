from URLKeyword import utils
if __name__ == "__main__":
    files=["Data-9000"]
    categorys=["rt_Entertainment",
               "rt_Politics",
               "rt_Sports",
               "rt_US",
               "rt_Business",
               "rt_ScienceAndTechnology",
               "rt_World",
               "rt_Unclassified",
               "rt_Health",
               "rt_Canada"]
    for data in utils.filesLineIter(files):
        print(data)