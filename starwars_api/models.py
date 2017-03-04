from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError

api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        
        """
        for key,val in json_data.items():
            setattr(self, key, val)
        
            

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        """
        json_obj=getattr(api_client,"get_{}".format(cls.RESOURCE_NAME))(resource_id)
        
        return cls(json_obj)

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        
        return eval('{}QuerySet'.format(cls.RESOURCE_NAME.title()))()


class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'

    def __init__(self, json_data):
        super(People, self).__init__(json_data)

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        self.current_page_count=0
        self.page_element_to_get=0
        self._count=0
        self._nextpage=None
        self.objects=[]
        
        #first time next is called
        if self.current_page_count is 0:
            self.current_page_count+=1
            self.objects=self._getNextPage()
        
        

    def __iter__(self):
        return self.__class__()

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        
        model_name=eval(self.__class__.RESOURCE_NAME.title())
        
        #get new page if you have reached the last element of the page
        if self.page_element_to_get == len(self.objects) :
  
            
            #check if there are pages still left and get next page if there are
            if self._nextpage is not 'null':

                self.current_page_count+=1
                self.page_element_to_get=0
                self.objects=
                #if you get error while trying to access next page raise error
                try:
                    self.objects=self._getNextPage()
                except SWAPIClientError:
                    raise StopIteration
                print self.page_element_to_get+1,len(self.objects) 
                
            else:
                raise StopIteration
        
        
    
        model_element=self.objects[self.page_element_to_get]
        self.page_element_to_get+=1
        
     
        
        return model_name(model_element)
        

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        return self._count
    
    def _getNextPage(self):
        
        obj=getattr(api_client,"get_{}".format(self.RESOURCE_NAME))(**{"page": self.current_page_count})
        self._nextpage=obj['next']
        self._count=obj['count']
        
        return obj['results']
    

        
        


class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))
