# frozen_string_literal: true

require 'httparty'
require 'json'
require 'logger'
require 'sinatra/base'
require 'sinatra/namespace'
require 'time'
require 'tzinfo'

# Defaults to Northpole
LATITUDE = ENV.fetch('LATITUDE', 90.00)
LONGITUDE = ENV.fetch('LONGITUDE', 135.00)

TIMEZONE = ENV.fetch('TIMEZONE', 'GMT')

HTTParty::Basement.default_options.update(verify: false)

# The main App class
class App < Sinatra::Base
  register Sinatra::Namespace

  set :logger, @logger
  set :bind, '0.0.0.0'

  def initialize(app = nil)
    super(app)

    @tz = TZInfo::Timezone.get(TIMEZONE)
    @logger = Logger.new($stdout)
    $stdout.sync = true
    @logger.info("LATITUDE: #{LATITUDE}")
    @logger.info("LONGITUDE: #{LONGITUDE}")
    @logger.info("TIMEZONE: #{TIMEZONE}")
  end

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
      sunrise_gmt = Time.parse("#{json['results']['sunrise']}  UTC")
      sunrise_local = @tz.to_local(sunrise_gmt)

      { 'results' => { 'sunrise' => sunrise_local.strftime('%k:%M').strip } }.to_json
    end

    get '/sunset' do
      today = Date.today
      data = HTTParty.get("https://api.sunrise-sunset.org/json?lat=#{LATITUDE}&lng=#{LONGITUDE}&date=#{today}").body
      json = JSON.parse(data)
      sunset_gmt = Time.parse("#{json['results']['sunset']}  UTC")
      sunset_local = @tz.to_local(sunset_gmt)

      { 'results' => { 'sunset' => sunset_local.strftime('%k:%M').strip } }.to_json
    end
  end

  # start the server if ruby file executed directly
  run! if app_file == $PROGRAM_NAME
end
