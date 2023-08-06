from rest_framework import serializers
from django_geo_db.models import Location, GeoCoordinate, Zipcode, Continent, Country, State, City, County, \
                                 LocationMap, LocationMapType


class GeoCoordinateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('geocoordinate-detail')
    class Meta:
        model = GeoCoordinate
        fields = ('geocoordinate_id', 'lat', 'lon', 'generated_name', 'url')


class ContinentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('continent-detail')
    class Meta:
        model = Continent
        fields = ('continent_id', 'name', 'url')


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('country-detail')
    class Meta:
        model = Country
        fields = ('country_id', 'continent', 'name', 'abbreviation', 'geocoordinate', 'url')


class CountySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('county-detail')
    class Meta:
        model = County
        fields = ('county_id', 'state', 'name', 'geocoordinate', 'generated_name', 'url')


class StateSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('state-detail')
    class Meta:
        model = State
        fields = ('state_id', 'country', 'name', 'abbreviation', 'geocoordinate', 'generated_name', 'url')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('city-detail')
    class Meta:
        model = City
        fields = ('city_id', 'state', 'county', 'name', 'geocoordinate', 'generated_name', 'url')


class ZipcodeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField('zipcode-detail')
    class Meta:
        model = Zipcode
        fields = ('zipcode_id', 'city', 'zipcode', 'geocoordinate', 'timezone', 'url')


class LocationSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField('location-detail')

    def get_lat(self, obj):
        return str(obj.get_geocoordinate().lat)

    def get_lon(self, obj):
        return str(obj.get_geocoordinate().lon)

    class Meta:
        model = Location
        fields = ('location_id', 'country', 'city', 'county', 'state', 'zipcode', 'geocoordinate', 'lat', 'lon', 'name', 'generated_name', 'url')


class LocationMapSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = LocationMap
        fields = ('type', 'map_file_url', 'location')


class LocationMapTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocationMapType
        fields = ('type',)


