"""
High level routing functionality
"""
import sql_queries
import path_finder
import mapquest_api


class hopper(object):
    
    def __init__(self):
        self.bay_area_range = (37.3333, 37.9736, -122.5311 , 121.9000)
        self.db = sql_queries.sql()
        self.finder = path_finder.path_finder()
        self.distance_api = mapquest_api.mapquest_api()
        
    def _cumsum(self, iterator, start = 1):
        """Cumulitve sum"""
        s = start
        yield s
        for elem in iterator:
            s = s + elem
            yield s
        
    def get_path(self, start_lat, start_long, yelp_rating, categories):
        listings, lengths = self.db.get_listings(start_lat, start_long, yelp_rating, categories, number = 6)
        coordinates = ['{0},{1}'.format(start_lat, start_long)]
        coordinates.extend('{0},{1}'.format(res[-4],res[-3]) for res in listings)
        sums = list(self._cumsum(lengths))
        common_groups = [range(sums[k], sums[k+1]) for k in range(len(sums) - 1)]
        print common_groups
        distances = self.distance_api.get_all_to_all_matrix(coordinates)
        shortest_length, path = self.finder.get_fastest_path(distances, common_groups, start = 0, stop = 0)
        return [listings[p - 1] for p in path]
    
    def get_coordinates(self, address):
        lat, long, quality = self.distance_api.get_latlong([address])[0]
        return lat,long

    def in_bay_area(self, lat, long):
        lat_min, lat_max, long_min, long_max = self.bay_area_range
        return (lat_min <= lat <= lat_max) and (long_min <= long <= long_max)

if __name__ == '__main__':
    import time
    hopper = hopper()
    
    def test1():
        start_lat,start_long = 37.524968,-122.2508315
        yelp_rating = 20#top percent
        categories = ['Post Offices','Nordstrom','Grocery','Drugstores']
        number = 6
        t1 = time.time()
        path_list = hopper.get_path(start_lat, start_long, yelp_rating, categories)
        print time.time() - t1
        for p in path_list:
            print p[1], p[2], p[3]
    
    def test2():
        start_lat,start_long = 37.524968,-122.2508315
        yelp_rating = 100
        entries = ['CVS']
        number = 6
        path_list = hopper.get_path(start_lat, start_long, yelp_rating, entries)
        for p in path_list:
            print p[1], p[2], p[3]
    test2()