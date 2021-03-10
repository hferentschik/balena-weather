# frozen_string_literal: true

require 'httparty'
require 'json'
require 'logger'
require 'sinatra'
require "sinatra/namespace"
require 'time'
require 'tzinfo'

logger = Logger.new($stdout)
$stdout.sync = true

set :logger, logger
set :bind, '0.0.0.0'

# Defaults to Northpole
LATITUDE = ENV.fetch('LATITUDE', 90.00)
LONGITUDE = ENV.fetch('LONGITUDE', 135.00)

TIMEZONE = ENV.fetch('TIMEZONE', 'GMT')

tz = TZInfo::Timezone.get(TIMEZONE)

logger.info("LATITUDE: #{LATITUDE}")
logger.info("LONGITUDE: #{LONGITUDE}")
logger.info("TIMEZONE: #{TIMEZONE}")

get '/' do
  'Welcome to the weather API'
end

namespace '/api/v1' do

  before do
    content_type 'application/json'
  end

  get '/sunrise' do
    today = Date.today
    data = HTTParty.get("https://api.sunrise-sunset.org/json?lat=#{LATITUDE}&lng=#{LONGITUDE}&date=#{today}").body
    json = JSON.parse(data)
    sunrise_gmt = Time.parse(json['results']['sunrise'] + " UTC")
    sunrise_local = tz.to_local(sunrise_gmt)

    { 'results' => {'sunrise' => sunrise_local.strftime('%k:%M').strip}}.to_json
  end

  get '/sunset' do
    today = Date.today
    data = HTTParty.get("https://api.sunrise-sunset.org/json?lat=#{LATITUDE}&lng=#{LONGITUDE}&date=#{today}").body
    json = JSON.parse(data)
    sunset_gmt = Time.parse(json['results']['sunset'] + " UTC")
    sunset_local = tz.to_local(sunset_gmt)

    { 'results' => {'sunset' => sunset_local.strftime('%k:%M').strip}}.to_json
  end
end