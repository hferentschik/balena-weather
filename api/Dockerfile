FROM balenalib/raspberrypi3-64:buster

RUN apt-get update \
 && apt-get install -y ruby wget vim \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN gem install bundler --without test

WORKDIR /app

COPY Gemfile /app/Gemfile
COPY Gemfile.lock /app/Gemfile.lock
RUN bundle config set --local without 'development test' \
 && bundle install

COPY server.rb /app

RUN useradd -ms /bin/bash weather
RUN chown -R weather:weather /app
USER weather

EXPOSE 4567
CMD [ "bundle", "exec", "ruby", "server.rb" ]
